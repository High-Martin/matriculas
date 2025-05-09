# filepath: /home/bgmartins/git/high-martin/matriculas/matriculasapp/dao/matricula_dao.py
from __future__ import annotations

from typing import TYPE_CHECKING

from matriculasapp.dao.core.dao import Dao
from matriculasapp.dao.core.query_builder import QueryBuilder
from matriculasapp.models import MatriculaModel

if TYPE_CHECKING:
    from psycopg2.extensions import connection


class MatriculaDao(Dao):
    """Classe que implementa o padrão de projeto DAO para a entidade Matricula.

    Esta classe fornece métodos para operações de banco de dados relacionadas à entidade Matricula.
    """

    def __init__(self, connection: connection) -> None:
        """Inicializa o DAO com conexão com o banco de dados PostgreSQL já configurada."""
        super().__init__(connection)
        self.table_name = "matriculas"

    def find_by_id(self, matricula_id: int | str) -> MatriculaModel | None:
        """Busca uma matrícula pelo ID.

        Args_:
            object_id (int | str): ID da matrícula

        Returns_:
            MatriculaModel | None: Dicionário com os dados da matrícula ou None se não encontrada
        """
        query_builder = QueryBuilder(self)
        result = query_builder.where("id", "=", str(matricula_id)).execute()

        if result and len(result) > 0:
            return MatriculaModel.from_dict(result[0])
        return None

    def update(self, object_id: int | str, matricula: MatriculaModel) -> bool:
        """Atualiza os dados de uma matrícula.

        Args:
            object_id (int | str): ID da matrícula
            matricula (MatriculaModel): Objeto modelo com os dados a serem atualizados

        Returns:
            bool: True se a atualização foi bem-sucedida, False caso contrário

        """
        # Converte o modelo para dicionário
        data_dict = matricula.to_dict()

        # Remove o ID do dicionário de dados, se presente
        data_dict.pop("id", None)

        if not data_dict:  # Se não sobrou nada para atualizar
            return False

        set_clause = ", ".join(f"{key} = %s" for key in data_dict)
        values = list(data_dict.values())
        values.append(object_id)  # Para a condição WHERE

        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
        cursor = self.execute_query(query, tuple(values))
        rows_affected = cursor.rowcount
        cursor.close()

        return rows_affected > 0

    def delete(self, object_id: int | str) -> bool:
        """Remove uma matrícula do banco de dados.

        Args:
            object_id (int | str): ID da matrícula

        Returns:
            bool: True se a remoção foi bem-sucedida, False caso contrário

        """
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        cursor = self.execute_query(query, (object_id,))
        rows_affected = cursor.rowcount
        cursor.close()

        return rows_affected > 0

    def create(self, matricula: MatriculaModel) -> MatriculaModel | None:
        """Cria uma nova matrícula no banco de dados.

        Args:
            matricula (MatriculaModel): MatriculaModel com os dados da matrícula

        Returns:
            Dict | None: Dicionário com os dados da matrícula criada, incluindo o ID,
            ou None em caso de falha

        """
        # Remove o ID se estiver presente, pois ele será gerado automaticamente
        data = matricula.to_dict()
        data.pop("id", None)

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
        cursor = self.execute_query(query, values)
        result = cursor.fetchone()
        cursor.close()

        if result:
            return MatriculaModel.from_dict(dict(result))
        return None

    def get_all(self, page: int = 1, page_size: int = 10) -> list[MatriculaModel]:
        """Retorna todas as matrículas com suporte a paginação.

        Args:
            page (int, optional): Número da página atual. Defaults to 1.
            page_size (int, optional): Tamanho da página. Defaults to 10.

        Returns:
            List[MatriculaModel]: Lista de matrículas para a página solicitada

        """
        query_builder = QueryBuilder(self)

        offset = (page - 1) * page_size
        results = query_builder.limit(page_size).offset(offset).execute()

        return [MatriculaModel.from_dict(row) for row in results]

    def filter(self, filters: dict, page: int = 1, page_size: int = 10) -> list[MatriculaModel]:
        """Busca matrículas com base em filtros específicos.

        Args:
            filters (Dict): Dicionário com os filtros a serem aplicados
            page (int, optional): Número da página atual. Defaults to 1.
            page_size (int, optional): Tamanho da página. Defaults to 10.

        Returns:
            List[Dict]: Lista de dicionários com os dados das matrículas encontradas

        """
        if not filters:
            return self.get_all(page=page, page_size=page_size)

        query_builder = QueryBuilder(self)
        for key, value in filters.items():
            if isinstance(value, str):
                query_builder.where(key, "ILIKE", value)
            else:
                query_builder.where(key, "=", value)

        offset = (page - 1) * page_size
        results = query_builder.limit(page_size).offset(offset).execute()

        return [MatriculaModel.from_dict(row) for row in results]

    def count_by_filter(self, filters: dict | None = None) -> int:
        """Conta o número de matrículas com base em filtros específicos.

        Args:
            filters (Dict, optional): Dicionário com os filtros a serem aplicados. Defaults to None.

        Returns:
            int: Número de matrículas encontradas

        """
        query_builder = QueryBuilder(self)

        if filters:
            for key, value in filters.items():
                if isinstance(value, str):
                    query_builder.where(key, "ILIKE", value)
                else:
                    query_builder.where(key, "=", value)

        return query_builder.count()

    def get_quantidade_alunos(self, ano: str, filters: dict) -> int:
        """Conta o número de alunos matriculados.

        Args:
            ano (int): Ano da matrícula
            filters (Dict, optional): Dicionário com os filtros a serem aplicados. Defaults to None.

        Returns:
            int: Número de alunos matriculados

        """
        query_builder = QueryBuilder(self)
        query_builder.select([f"matriculas_{ano}"])

        for key, value in filters.items():
            if isinstance(value, str):
                query_builder.where(key, "ILIKE", value)
            else:
                query_builder.where(key, "=", value)

        return query_builder.count()
