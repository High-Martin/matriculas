from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import View

from matriculasapp.dao.dao_factory import DaoFactory


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
        dao_factory = DaoFactory()
        matricula_dao = dao_factory.get_matricula_dao()

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


class ListarCursosView(View):
    """View para listar cursos (a ser implementada no futuro)."""

    template_name = "matriculasapp/listar_cursos.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Processa requisições GET para exibir a página de cursos em desenvolvimento.

        Args:
            request: O objeto de requisição HTTP

        Returns:
            Uma resposta HTTP com o template renderizado

        """
        context = {"active_menu": "cursos"}
        return render(request, self.template_name, context)


class ListarAlunosView(View):
    """View para listar alunos (a ser implementada no futuro)."""

    template_name = "matriculasapp/listar_alunos.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Processa requisições GET para exibir a página de alunos em desenvolvimento.

        Args:
            request: O objeto de requisição HTTP

        Returns:
            Uma resposta HTTP com o template renderizado

        """
        context = {"active_menu": "alunos"}
        return render(request, self.template_name, context)
