"""URL configuration for matriculados project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.contrib import admin
from django.urls import path

from matriculasapp.views.api import (
    CountAlunosView,
    ListFiltroAlunosView,
    ListFiltroCursosView,
    RankingCursosView,
)
from matriculasapp.views.core import (
    DashBoardView,
    ListarMatriculasView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", DashBoardView.as_view(), name="dashboard"),
    path("matriculas/", ListarMatriculasView.as_view(), name="listar_matriculas"),
    path("dashboard/", DashBoardView.as_view(), name="dashboard"),
    # API URLs
    path("dashboard/count_alunos/", CountAlunosView.as_view(), name="count_alunos"),
    path("dashboard/ranking_cursos/", RankingCursosView.as_view(), name="ranking_cursos"),
    path("dashboard/filtro_alunos/", ListFiltroAlunosView.as_view(), name="filtro_alunos"),
    path("dashboard/filtro_cursos/", ListFiltroCursosView.as_view(), name="filtro_cursos"),
]
