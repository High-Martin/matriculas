from __future__ import annotations

from django.db import models

# Create your models here.


class Matricula(models.Model):
    estado = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    ies = models.CharField(max_length=255, blank=True, null=True)
    sigla = models.CharField(max_length=50, blank=True, null=True)
    organizacao = models.CharField(max_length=100, blank=True, null=True)
    categoria_administrativa = models.CharField(max_length=100, blank=True, null=True)
    nome_curso = models.CharField(max_length=255, blank=True, null=True)
    nome_detalhado_curso = models.CharField(max_length=255, blank=True, null=True)
    modalidade = models.CharField(max_length=50, blank=True, null=True)
    grau = models.CharField(max_length=100, blank=True, null=True)
    matriculas_2014 = models.IntegerField(blank=True, null=True)
    matriculas_2015 = models.IntegerField(blank=True, null=True)
    matriculas_2016 = models.IntegerField(blank=True, null=True)
    matriculas_2017 = models.IntegerField(blank=True, null=True)
    matriculas_2018 = models.IntegerField(blank=True, null=True)
    matriculas_2019 = models.IntegerField(blank=True, null=True)
    matriculas_2020 = models.IntegerField(blank=True, null=True)
    matriculas_2021 = models.IntegerField(blank=True, null=True)
    matriculas_2022 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "matriculas"
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"

    def __str__(self):
        return f"{self.nome_curso or 'Sem nome'} - {self.ies or 'Sem IES'} ({self.cidade or 'Sem cidade'}/{self.estado or 'Sem estado'})"


# Classe model crua para Matricula sem dependências do Django
class MatriculaModel:
    """Modelo crua para representar a entidade Matricula sem dependências do Django.

    Esta classe serve como um objeto de transferência de dados (DTO) para operações de DAO.
    """

    def __init__(
        self,
        id: int | None = None,
        estado: str | None = None,
        cidade: str | None = None,
        ies: str | None = None,
        sigla: str | None = None,
        organizacao: str | None = None,
        categoria_administrativa: str | None = None,
        nome_curso: str | None = None,
        nome_detalhado_curso: str | None = None,
        modalidade: str | None = None,
        grau: str | None = None,
        matriculas_2014: int | None = None,
        matriculas_2015: int | None = None,
        matriculas_2016: int | None = None,
        matriculas_2017: int | None = None,
        matriculas_2018: int | None = None,
        matriculas_2019: int | None = None,
        matriculas_2020: int | None = None,
        matriculas_2021: int | None = None,
        matriculas_2022: int | None = None,
    ):
        self.id = id
        self.estado = estado
        self.cidade = cidade
        self.ies = ies
        self.sigla = sigla
        self.organizacao = organizacao
        self.categoria_administrativa = categoria_administrativa
        self.nome_curso = nome_curso
        self.nome_detalhado_curso = nome_detalhado_curso
        self.modalidade = modalidade
        self.grau = grau
        self.matriculas_2014 = matriculas_2014
        self.matriculas_2015 = matriculas_2015
        self.matriculas_2016 = matriculas_2016
        self.matriculas_2017 = matriculas_2017
        self.matriculas_2018 = matriculas_2018
        self.matriculas_2019 = matriculas_2019
        self.matriculas_2020 = matriculas_2020
        self.matriculas_2021 = matriculas_2021
        self.matriculas_2022 = matriculas_2022

    @classmethod
    def from_dict(cls, data: dict) -> MatriculaModel:
        """Cria uma instância de MatriculaModel a partir de um dicionário."""
        return cls(**data)

    def to_dict(self) -> dict:
        """Convert a instância em um dicionário."""
        return {
            "id": self.id,
            "estado": self.estado,
            "cidade": self.cidade,
            "ies": self.ies,
            "sigla": self.sigla,
            "organizacao": self.organizacao,
            "categoria_administrativa": self.categoria_administrativa,
            "nome_curso": self.nome_curso,
            "nome_detalhado_curso": self.nome_detalhado_curso,
            "modalidade": self.modalidade,
            "grau": self.grau,
            "matriculas_2014": self.matriculas_2014,
            "matriculas_2015": self.matriculas_2015,
            "matriculas_2016": self.matriculas_2016,
            "matriculas_2017": self.matriculas_2017,
            "matriculas_2018": self.matriculas_2018,
            "matriculas_2019": self.matriculas_2019,
            "matriculas_2020": self.matriculas_2020,
            "matriculas_2021": self.matriculas_2021,
            "matriculas_2022": self.matriculas_2022,
        }

    def __str__(self) -> str:
        """Representação em string da instância."""
        return (
            f"{self.nome_curso or 'Sem nome'} - {self.ies or 'Sem IES'} "
            f"({self.cidade or 'Sem cidade'}/{self.estado or 'Sem estado'})"
        )
