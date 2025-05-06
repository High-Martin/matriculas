from django.contrib import admin
from .models import Matricula

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'ies', 'cidade', 'estado', 'modalidade', 'grau', 
                    'matriculas_2022', 'matriculas_2021', 'matriculas_2020', 
                    'matriculas_2019', 'matriculas_2018', 'matriculas_2017', 
                    'matriculas_2016', 'matriculas_2015', 'matriculas_2014')
    list_filter = ('estado', 'modalidade', 'grau')
    search_fields = ('nome_curso', 'ies', 'cidade', 'estado')
    ordering = ('-matriculas_2022',)
    list_per_page = 50
