import logging

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from matriculasapp.dao.core.dao_factory import DaoFactory
from matriculasapp.models.filtro_alunos import FiltroAlunos
from matriculasapp.models.filtro_cursos import FiltroCursos

# Configura um logger específico para este módulo
logger = logging.getLogger(__name__)


class CountAlunosView(View):
    """View API que retorna a contagem de alunos com base em filtros.

    Parâmetros de URL aceitos:
        ano: Ano da matrícula
        modalidade: Modalidade do curso (presencial, ead, etc)
        estado: Estado da instituição
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """Processa requisições GET e retorna JSON com contagem de alunos.

        Args:
            request: O objeto de requisição HTTP

        Returns:
            Uma resposta JSON com o resultado da contagem

        """
        # Obter parâmetros da URL
        ano = request.GET.get("ano")
        modalidade = request.GET.get("modalidade")
        estado = request.GET.get("estado")

        # Aqui seria implementada a lógica de contagem usando o DAO
        # Por enquanto, apenas retornamos um OK conforme solicitado
        filters = {}
        if modalidade:
            filters["modalidade"] = modalidade
        if estado:
            filters["estado"] = estado

        matricula_dao = DaoFactory().get_matricula_dao()
        count_alunos = matricula_dao.get_quantidade_alunos(ano, filters)

        filtro_dao = DaoFactory().get_filtro_alunos_dao()
        filtro_aluno = FiltroAlunos(ano=ano, modalidade=modalidade, estado=estado)
        filtro_dao.create(filtro_aluno)

        return JsonResponse(
            {
                "status": "ok",
                "count": count_alunos,
            }
        )


class RankingCursosView(View):
    """View API que retorna o ranking dos 10 cursos com  mais matriculas.

    Parâmetros de URL aceitos:
        modalidade: Modalidade do curso (presencial, ead, etc)
        estado: Estado da instituição

    OBS: O ano é fixo 2022.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        """Processa requisições GET e retorna JSON com o ranking de cursos.

        Args:
            request: O objeto de requisição HTTP

        Returns:
            Uma resposta JSON com o resultado do ranking

        """
        # Obter parâmetros da URL
        modalidade = request.GET.get("modalidade")
        estado = request.GET.get("estado")

        # Aqui seria implementada a lógica de contagem usando o DAO
        # Por enquanto, apenas retornamos um OK conforme solicitado
        filters = {}
        if modalidade:
            filters["modalidade"] = modalidade
        if estado:
            filters["estado"] = estado

        matricula_dao = DaoFactory().get_matricula_dao()
        ranking_cursos = matricula_dao.get_ranking_cursos(2022, 10, filters)

        filtro_dao = DaoFactory().get_filtro_cursos_dao()
        filtro_curso = FiltroCursos(modalidade=modalidade, estado=estado)
        filtro_dao.create(filtro_curso)

        return JsonResponse(
            {
                "status": "ok",
                "cursos": ranking_cursos,
            }
        )


class ListFiltroAlunosView(View):
    """View API que retorna os últimos filtros de alunos pesquisados."""

    def get(self, _: HttpRequest) -> JsonResponse:
        """Processa requisições GET e retorna JSON com os últimos filtros de alunos."""
        try:
            filtro_alunos_dao = DaoFactory().get_filtro_alunos_dao()
            ultimos_filtros_alunos = filtro_alunos_dao.list_latest()
            filtros_dict = [filtro.to_dict() for filtro in ultimos_filtros_alunos]
            return JsonResponse({"status": "ok", "filtros_alunos": filtros_dict})
        except Exception:  # Captura genérica para simplificar, idealmente mais específica
            logger.exception("Erro ao buscar filtros de alunos:")
            return JsonResponse(
                {"status": "error", "message": "Ocorreu um erro ao processar sua solicitação."},
                status=500,
            )


class ListFiltroCursosView(View):
    """View API que retorna os últimos filtros de cursos pesquisados."""

    def get(self, _: HttpRequest) -> JsonResponse:
        """Processa requisições GET e retorna JSON com os últimos filtros de cursos."""
        try:
            filtro_cursos_dao = DaoFactory().get_filtro_cursos_dao()
            ultimos_filtros_cursos = filtro_cursos_dao.list_latest()
            filtros_dict = [filtro.to_dict() for filtro in ultimos_filtros_cursos]
            return JsonResponse({"status": "ok", "filtros_cursos": filtros_dict})
        except Exception:  # Captura genérica para simplificar, idealmente mais específica
            logger.exception("Erro ao buscar filtros de cursos:")
            return JsonResponse(
                {"status": "error", "message": "Ocorreu um erro ao processar sua solicitação."},
                status=500,
            )
