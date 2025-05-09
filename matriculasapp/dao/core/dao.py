from __future__ import annotations

from typing import TYPE_CHECKING

import psycopg2
import psycopg2.extras  # Para permitir acesso a colunas por nome

from matriculasapp.utils.exceptions import DatabaseConnectionError

if TYPE_CHECKING:
    from psycopg2.extensions import connection, cursor


class Dao:
    """Classe abstrata que implementa o padrão de projeto DAO (Data Access Object).

    Esta classe fornece uma interface para operações de banco de dados.
    """

    table_name: str

    def __init__(self, connection: connection) -> None:
        """Inicializa o DAO com conexão com o banco de dados PostgreSQL já configurada."""
        self.connection = connection

    def execute_query(self, query: str, params: tuple | None = None) -> cursor:
        """Executa uma consulta SQL no PostgreSQL.

        Args_:
            query (str): Consulta SQL a ser executada
            params (tuple, optional): Parâmetros para a consulta

        Returns)_:
            cursor: Cursor para os resultados da consulta
        """
        # print(f"Executando consulta: {query} com parâmetros: {params}")
        try:
            # Usar DictCursor para permitir acesso às colunas pelo nome
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()
        except psycopg2.Error as e:
            if self.connection:
                self.connection.rollback()
            msg = f"Erro ao executar a consulta: {e}"
            raise DatabaseConnectionError(msg) from e
        else:
            return cursor
