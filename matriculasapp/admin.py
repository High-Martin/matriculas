from __future__ import annotations

from django.contrib import admin
from django.db import models


class MatriculaDjango(models.Model):
    estado: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    cidade: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    ies: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    sigla: models.CharField = models.CharField(max_length=50, blank=True, null=True)
    organizacao: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    categoria_administrativa: models.CharField = models.CharField(
        max_length=100, blank=True, null=True
    )
    nome_curso: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    nome_detalhado_curso: models.CharField = models.CharField(max_length=255, blank=True, null=True)
    modalidade: models.CharField = models.CharField(max_length=50, blank=True, null=True)
    grau: models.CharField = models.CharField(max_length=100, blank=True, null=True)
    matriculas_2014: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2015: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2016: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2017: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2018: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2019: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2020: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2021: models.IntegerField = models.IntegerField(blank=True, null=True)
    matriculas_2022: models.IntegerField = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "matriculas"
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"

    def __str__(self):
        return f"{self.nome_curso or 'Sem nome'} - {self.ies or 'Sem IES'} ({self.cidade or 'Sem cidade'}/{self.estado or 'Sem estado'})"


@admin.register(MatriculaDjango)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_curso",
        "ies",
        "cidade",
        "estado",
        "modalidade",
        "grau",
        "matriculas_2022",
        "matriculas_2021",
        "matriculas_2020",
        "matriculas_2019",
        "matriculas_2018",
        "matriculas_2017",
        "matriculas_2016",
        "matriculas_2015",
        "matriculas_2014",
    )
    list_filter = ("estado", "modalidade", "grau")
    search_fields = ("nome_curso", "ies", "cidade", "estado")
    ordering = ("-matriculas_2022",)
    list_per_page = 50
