from django.http import HttpRequest, JsonResponse
from django.views.generic import View

from matriculasapp.dao.core.dao_factory import DaoFactory


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

        matricula_dao = DaoFactory().get_dao("matricula")
        count_alunos = matricula_dao.get_quantidade_alunos(ano, filters)

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

        matricula_dao = DaoFactory().get_dao("matricula")
        ranking_cursos = matricula_dao.get_ranking_cursos(2022, 10, filters)

        return JsonResponse(
            {
                "status": "ok",
                "cursos": ranking_cursos,
            }
        )
