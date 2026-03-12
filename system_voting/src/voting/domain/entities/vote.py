"""
Entidad de Voto - Dominio Puro
Vertical Slicing + Hexagonal Architecture
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Vote:
    """Entidad de Voto para Consulta Popular"""

    id_consult: str
    id_member: str
    id_party: str
    id_auth: str
    value_vote: bool
    comment: Optional[str] = None
    id: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        if not self.id_consult:
            raise ValueError("El ID de consulta es requerido")

        if not self.id_member:
            raise ValueError("El ID del miembro es requerido")

        if not self.id_party:
            raise ValueError("El ID del partido es requerido")

        if not self.id_auth:
            raise ValueError("El ID de la autoridad es requerido")


@dataclass
class CreateVoteCommand:
    """Comando para crear un voto"""

    id_consult: str
    id_member: str
    id_party: str
    id_auth: str
    value_vote: bool
    comment: Optional[str] = None
