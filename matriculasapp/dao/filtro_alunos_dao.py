from __future__ import annotations

from typing import TYPE_CHECKING

from matriculasapp.dao.core.dao import Dao
from matriculasapp.dao.core.query_builder import QueryBuilder  # Importa o QueryBuilder
from matriculasapp.models.filtro_alunos import FiltroAlunos

if TYPE_CHECKING:
    from psycopg2.extensions import connection


class FiltroAlunosDao(Dao):
    """DAO para a tabela filtro_aluno."""

    def __init__(self, connection: connection) -> None:
        """Inicializa o DAO com conexão com o banco de dados PostgreSQL já configurada."""
        super().__init__(connection)
        self.table_name = "filtro_aluno"  # Corrigido nome da tabela

    def migrate_table(self) -> None:
        """Cria a tabela FILTRO_ALUNO no banco de dados."""
        sql = """
            CREATE TABLE IF NOT EXISTS filtro_aluno (
                id SERIAL PRIMARY KEY,
                ano VARCHAR(255),
                modalidade VARCHAR(255),
                estado VARCHAR(255)
            )
            """
        self.execute_query(sql)

    def create(self, filtro_aluno: FiltroAlunos) -> FiltroAlunos:
        """Cria um novo registro de filtro_aluno no banco de dados.

        Args:
            filtro_aluno: O objeto FiltroAlunos a ser criado.

        Returns:
            O objeto FiltroAlunos com o ID atualizado.

        """
        # self.table_name é um atributo da classe, considerado seguro para interpolação aqui.
        sql = f"""
            INSERT INTO {self.table_name} (ano, modalidade, estado)
            VALUES (%s, %s, %s)
            RETURNING id
        """
        params = (
            filtro_aluno.ano,
            filtro_aluno.modalidade,
            filtro_aluno.estado,
        )
        cursor = self.execute_query(sql, params)
        result_row = cursor.fetchone()  # Retorna uma tupla (ou DictRow) ou None

        if result_row is not None:
            # Assumindo que 'id' é o primeiro campo retornado por RETURNING id
            filtro_aluno.id = result_row[0]
        return filtro_aluno

    def list_latest(self, limit: int = 2) -> list[FiltroAlunos]:
        """Lista os últimos registros de filtro_aluno do banco de dados usando QueryBuilder.

        Args:
            limit: O número máximo de registros a serem retornados.

        Returns:
            Uma lista de objetos FiltroAlunos.

        """
        qb = QueryBuilder(self)
        # QueryBuilder.execute() já retorna uma lista de dicionários.
        result_rows_as_dicts = (
            qb.select(["id", "ano", "modalidade", "estado"])
            .order_by("id", "DESC")
            .limit(limit)
            .execute()
        )

        # Converte a lista de dicionários em uma lista de objetos FiltroAlunos
        return [FiltroAlunos.from_dict(row_dict) for row_dict in result_rows_as_dicts]
