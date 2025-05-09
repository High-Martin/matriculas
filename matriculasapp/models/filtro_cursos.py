class FiltroCursos:
    """Representa tabela FILTRO_CURSOS do banco de dados."""

    def __init__(
        self,
        id: int | None = None,
        modalidade: str | None = None,
        estado: str | None = None,
    ):
        self.id = id
        self.modalidade = modalidade
        self.estado = estado

    @classmethod
    def from_dict(cls, data: dict) -> "FiltroCursos":
        """Cria uma instância de FiltroCursos a partir de um dicionário."""
        return cls(**data)

    def to_dict(self) -> dict:
        """Convert a instância em um dicionário."""
        return {
            "id": self.id,
            "modalidade": self.modalidade,
            "estado": self.estado,
        }

    def __str__(self) -> str:
        """Representação em string da instância."""
        return f"FiltroCursos(id={self.id}, modalidade={self.modalidade}, estado={self.estado})"
