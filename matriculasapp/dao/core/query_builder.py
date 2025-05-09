from typing import Any

from matriculasapp.dao.core.dao import Dao


class QueryBuilder:
    """Classe interna para construção de consultas SQL."""

    def __init__(self, dao: Dao) -> None:
        """Inicializa o construtor de queries.

        Args:
            dao: Instância do MatriculaDao que contém a conexão

        """
        self.dao = dao
        self.select_columns = ["*"]
        self.where_clauses: list[str] = []
        self.values: list[object] = []
        self.order_by_clause: str | None = None
        self.limit_value: int | None = None
        self.offset_value: int | None = None
        self.group_by_clause: str | None = None

    def select(self, columns: list[str]) -> "QueryBuilder":
        """Define as colunas a serem selecionadas na query.

        Args:
            columns: Lista de nomes das colunas

        Returns:
            Referência ao próprio builder para encadeamento

        """
        self.select_columns = columns
        return self

    def where(self, column: str, operator: str, value: str) -> "QueryBuilder":
        """Adiciona uma condição WHERE à consulta.

        Args:
            column: Nome da coluna
            operator: Operador de comparação (=, >, <, LIKE, etc)
            value: Valor para comparação

        Returns:
            Referência ao próprio builder para encadeamento

        """
        # Para valores de texto com operadores LIKE/ILIKE, adicionar % automaticamente
        if (
            operator.upper() in ("LIKE", "ILIKE")
            and isinstance(value, str)
            and not (value.startswith("%") or value.endswith("%"))
        ):
            value = f"%{value}%"

        self.where_clauses.append(f"{column} {operator} %s")
        self.values.append(value)
        return self

    def order_by(self, column: str, direction: str = "ASC") -> "QueryBuilder":
        """Define a ordenação dos resultados.

        Args:
            column: Coluna para ordenação
            direction: Direção da ordenação (ASC ou DESC)

        Returns:
            Referência ao próprio builder para encadeamento

        """
        self.order_by_clause = f"{column} {direction}"
        return self

    def limit(self, limit: int) -> "QueryBuilder":
        """Define o limite de registros retornados.

        Args:
            limit: Número máximo de registros

        Returns:
            Referência ao próprio builder para encadeamento

        """
        self.limit_value = limit
        return self

    def offset(self, offset: int) -> "QueryBuilder":
        """Define o deslocamento para paginação.

        Args:
            offset: Número de registros a pular

        Returns:
            Referência ao próprio builder para encadeamento

        """
        self.offset_value = offset
        return self

    def group_by(self, columns: list[str]) -> "QueryBuilder":
        """Define agrupamento de resultados.

        Args:
            columns: Lista de colunas para agrupamento

        Returns:
            Referência ao próprio builder para encadeamento

        """
        self.group_by_clause = ", ".join(columns)
        return self

    def build_query(self) -> tuple[str, list]:
        """Constrói a query SQL com base nos componentes definidos.

        Returns:
            Tupla contendo a string da consulta SQL e a lista de valores para os parâmetros

        """
        select_clause = ", ".join(self.select_columns)
        query = f"SELECT {select_clause} FROM {self.dao.table_name}"

        if self.where_clauses:
            where_clause = " AND ".join(self.where_clauses)
            query += f" WHERE {where_clause}"

        if self.group_by_clause:
            query += f" GROUP BY {self.group_by_clause}"

        if self.order_by_clause:
            query += f" ORDER BY {self.order_by_clause}"

        if self.limit_value:
            query += " LIMIT %s"
            self.values.append(self.limit_value)

        if self.offset_value:
            query += " OFFSET %s"
            self.values.append(self.offset_value)

        return query, self.values

    def execute(self) -> list[dict]:
        """Executa a consulta e retorna os resultados brutos como dicionários.

        Returns:
            Lista de dicionários, cada um representando um registro

        """
        query, values = self.build_query()
        cursor = self.dao.execute_query(query, tuple(values) if values else None)
        results = cursor.fetchall()
        cursor.close()

        return [dict(row) for row in results]

    def execute_scalar(self) -> Any | None:
        """Executa a consulta e retorna um valor único (primeira coluna do primeiro registro).

        Returns:
            Valor da primeira coluna do primeiro registro ou None se não houver resultados

        """
        query, values = self.build_query()
        cursor = self.dao.execute_query(query, tuple(values) if values else None)
        result = cursor.fetchone()
        cursor.close()

        return result[0] if result else None

    def _execute_aggregate(self, aggregate_columns: list[str]) -> int:
        """Método auxiliar para executar funções de agregação.

        Args:
            aggregate_columns: Lista com as colunas da função de agregação

        Returns:
            Resultado da função de agregação ou 0 se não houver resultados

        """
        # Salvar estado original
        original_columns = self.select_columns
        original_limit = self.limit_value
        original_offset = self.offset_value

        # Configurar para agregação
        self.select_columns = aggregate_columns
        self.limit_value = None
        self.offset_value = None

        # Executar consulta
        result = self.execute_scalar()

        # Restaurar estado original
        self.select_columns = original_columns
        self.limit_value = original_limit
        self.offset_value = original_offset

        return result or 0

    def count(self) -> int:
        """Executa uma consulta COUNT com os mesmos filtros.

        Returns:
            Número de registros que correspondem aos filtros

        """
        return self._execute_aggregate([f"COUNT({','.join(self.select_columns)})"])

    def sum(self, column: str) -> int:
        """Executa uma consulta SUM com os mesmos filtros.

        Args:
            column: Nome da coluna a ser somada

        Returns:
            Soma dos valores da coluna especificada

        """
        return self._execute_aggregate([f"SUM({column})"])
