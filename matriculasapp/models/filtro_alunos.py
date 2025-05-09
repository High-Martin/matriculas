class FiltroAlunos:
    """Representa tabela FILTRO_Alunos do banco de dados."""

    def __init__(
        self,
        id: int | None = None,
        ano: str | None = None,
        modalidade: str | None = None,
        estado: str | None = None,
    ):
        self.id = id
        self.ano = ano
        self.modalidade = modalidade
        self.estado = estado

    @classmethod
    def from_dict(cls, data: dict) -> "FiltroAlunos":
        """Cria uma instância de FiltroAlunos a partir de um dicionário."""
        return cls(**data)

    def to_dict(self) -> dict:
        """Convert a instância em um dicionário."""
        return {
            "id": self.id,
            "ano": self.ano,
            "modalidade": self.modalidade,
            "estado": self.estado,
        }

    def __str__(self) -> str:
        """Representação em string da instância."""
        return f"FiltroAlunos(id={self.id}, modalidade={self.modalidade}, estado={self.estado})"
