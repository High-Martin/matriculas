from __future__ import annotations


# Classe model crua para Matricula sem dependências do Django
class Matricula:
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
    def from_dict(cls, data: dict) -> Matricula:
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
