import psycopg2
import psycopg2.extras  # Para permitir acesso a colunas por nome
from django.conf import settings
from psycopg2.extensions import connection

from matriculasapp.dao.core.dao import Dao
from matriculasapp.dao.filtro_alunos_dao import FiltroAlunosDao
from matriculasapp.dao.filtro_cursos_dao import FiltroCursosDao
from matriculasapp.dao.matricula_dao import MatriculaDao
from matriculasapp.utils.exceptions import DatabaseConnectionError


class DaoFactory:
    """Classe responsável por criar conexão com banco de dados e instâncias de DAOs.

    Cria uma conexão com o banco de dados PostgreSQL e fornece métodos para
    obter instâncias de DAOs específicos que implementam operações de
    acesso a dados.
    """

    def __init__(self) -> None:
        """Inicializa o DAO com as credenciais para o banco de dados PostgreSQL.

        Args_

            dbname (str): Nome do banco de dados
        """
        try:
            data_base = settings.DATABASES["default"]
            self.dbname = data_base["NAME"]
            self.user = data_base["USER"]
            self.password = data_base["PASSWORD"]
            self.host = data_base["HOST"]
            self.port = data_base["PORT"]
            self.connection: connection | None = None
        except KeyError as e:
            msg = f"Erro ao acessar as configurações do banco de dados: {e}"
            raise KeyError(msg) from e

    def _connect(self) -> connection:
        """Estabelece uma conexão com o banco de dados PostgreSQL.

        Returns_
            Connection: Objeto de conexão com o banco de dados
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
        except psycopg2.Error as e:
            msg = f"Erro ao conectar ao banco de dados PostgreSQL: {e}"
            raise DatabaseConnectionError(msg) from e
        else:
            return self.connection

    def _disconnect(self) -> None:
        """Fecha a conexão com o banco de dados."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def _get_connection(self) -> connection:
        """Obtém uma conexão com o banco de dados.

        Returns_:
            Connection: Objeto de conexão com o banco de dados
        """
        if not self.connection:
            return self._connect()
        return self.connection

    def get_matricula_dao(self) -> MatriculaDao:
        """Obtém uma instância do DAO de matrícula."""
        return MatriculaDao(self._get_connection())

    def get_filtro_alunos_dao(self) -> FiltroAlunosDao:
        """Obtém uma instância do DAO de filtro de alunos."""
        return FiltroAlunosDao(self._get_connection())

    def get_filtro_cursos_dao(self) -> FiltroCursosDao:
        """Obtém uma instância do DAO de filtro de cursos."""
        return FiltroCursosDao(self._get_connection())

    def get_dao(self, table_name: str) -> Dao:
        """Obtém uma instância do DAO para a tabela especificada.

        Args:
            table_name (str): Nome da tabela

        Returns:
            MatriculaDao: Instância do DAO para a tabela especificada

        """
        tables_map = {
            "matricula": self.get_matricula_dao,
            "filtro_aluno": self.get_filtro_alunos_dao,
            "filtro_cursos": self.get_filtro_cursos_dao,
        }
        dao = tables_map.get(table_name)

        if dao is None:
            msg = f"DAO para a tabela {table_name} não encontrado."
            raise ValueError(msg)

        return dao()
