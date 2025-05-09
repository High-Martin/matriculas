from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from matriculasapp.dao.core.dao_factory import DaoFactory


class ListarMatriculasView(View):
    """View para listar matrículas com suporte a paginação."""

    template_name = "matriculasapp/listar_matriculas.html"
    page_size = 10  # Número de itens por página

    def get(self, request: HttpRequest) -> HttpResponse:
        """Processa requisições GET para exibir a lista de matrículas.

        Args:
            request: O objeto de requisição HTTP

        Returns:
            Uma resposta HTTP com o template renderizado

        """
        # Obter parâmetros da página
        page = request.GET.get("page", 1)
        try:
            page = int(page)
            page = max(page, 1)
        except ValueError:
            page = 1

        # Obter filtros da URL (se houver)
        filters = {}
        for param in ["estado", "cidade", "modalidade", "grau", "nome_curso"]:
            if request.GET.get(param):
                filters[param] = request.GET[param]

        # Buscar dados usando o DAO
        matricula_dao = DaoFactory().get_matricula_dao()

        # Obter matrículas com base nos filtros
        if filters:
            matriculas = matricula_dao.filter(filters, page, self.page_size)
            total_registros = matricula_dao.count_by_filter(filters)
        else:
            matriculas = matricula_dao.get_all(page, self.page_size)
            total_registros = matricula_dao.count_by_filter()

        # Configurar paginação
        total_pages = (total_registros + self.page_size - 1) // self.page_size

        # Dados para enviar ao template
        context = {
            "matriculas": matriculas,
            "page": page,
            "total_pages": total_pages,
            "filtros": filters,
            "total_registros": total_registros,
            "active_menu": "matriculas",  # Indica o item ativo no menu
        }

        return render(request, self.template_name, context)


class DashBoardView(View):
    """View para listar cursos (a ser implementada no futuro)."""

    template_name = "matriculasapp/dashboard.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Processa requisições GET para exibir infornmações gerais da aplicação.

        Args:
            request: O objeto de requisição HTTP

        Returns:
            Uma resposta HTTP com o template renderizado

        """
        matricula_dao = DaoFactory().get_matricula_dao()
        count_alunos: int = matricula_dao.get_quantidade_alunos()
        formated_count: str = f"{count_alunos:,}".replace(",", ".")

        ranking_cursos = matricula_dao.get_ranking_cursos(2022, 10)

        context = {
            "active_menu": "dashboard",
            "ranking_cursos": ranking_cursos,
            "count_alunos": formated_count,
            "ano_default": 2022,
            "anos": [
                2014,
                2015,
                2016,
                2017,
                2018,
                2019,
                2020,
                2021,
                2022,
            ],
        }
        return render(request, self.template_name, context)
