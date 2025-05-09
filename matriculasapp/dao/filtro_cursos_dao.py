from __future__ import annotations

from typing import TYPE_CHECKING

from matriculasapp.dao.core.dao import Dao
from matriculasapp.dao.core.query_builder import QueryBuilder  # Importa o QueryBuilder
from matriculasapp.models.filtro_cursos import FiltroCursos

if TYPE_CHECKING:
    from psycopg2.extensions import connection


class FiltroCursosDao(Dao):
    """DAO para a tabela filtro_cursos."""

    def __init__(self, connection: connection) -> None:
        """Inicializa o DAO com conexão com o banco de dados PostgreSQL já configurada."""
        super().__init__(connection)
        self.table_name = "filtro_cursos"  # Corrigido nome da tabela

    def migrate_table(self) -> None:
        """Cria a tabela FILTRO_CURSOS no banco de dados."""
        sql = """
            CREATE TABLE IF NOT EXISTS filtro_cursos (
                id SERIAL PRIMARY KEY,
                modalidade VARCHAR(255),
                estado VARCHAR(255)
            )
            """
        self.execute_query(sql)

    def create(self, filtro_cursos: FiltroCursos) -> FiltroCursos:
        """Cria um novo registro de filtro_cursos no banco de dados.

        Args:
            filtro_cursos: O objeto FiltroCursos a ser criado.

        Returns:
            O objeto FiltroCursos com o ID atualizado.

        """
        # self.table_name é um atributo da classe, considerado seguro para interpolação aqui.
        sql = f"""
            INSERT INTO {self.table_name} (modalidade, estado)
            VALUES (%s, %s)
            RETURNING id
        """
        params = (
            filtro_cursos.modalidade,
            filtro_cursos.estado,
        )
        cursor = self.execute_query(sql, params)
        result_row = cursor.fetchone()  # Retorna uma tupla (ou DictRow) ou None

        if result_row is not None:
            # Assumindo que 'id' é o primeiro campo retornado por RETURNING id
            filtro_cursos.id = result_row[0]
        return filtro_cursos

    def list_latest(self, limit: int = 2) -> list[FiltroCursos]:
        """Lista os últimos registros de filtro_cursos do banco de dados usando QueryBuilder.

        Args:
            limit: O número máximo de registros a serem retornados.

        Returns:
            Uma lista de objetos FiltroCursos.

        """
        qb = QueryBuilder(self)
        # QueryBuilder.execute() já retorna uma lista de dicionários.
        result_rows_as_dicts = (
            qb.select(["id", "modalidade", "estado"]).order_by("id", "DESC").limit(limit).execute()
        )

        # Converte a lista de dicionários em uma lista de objetos FiltroCursos
        return [FiltroCursos.from_dict(row_dict) for row_dict in result_rows_as_dicts]
