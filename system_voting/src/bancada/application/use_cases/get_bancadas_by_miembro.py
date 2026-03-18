from typing import List
from ...domain.entities.bancada import Bancada
from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class GetBancadasByMiembroUseCase:
    """Caso de uso: Obtener bancadas por miembro (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self, id_miembro: str) -> List[Bancada]:
        if not id_miembro or len(id_miembro) != 36:
            raise ValueError(
                "El ID del miembro debe ser un UUID válido (36 caracteres)"
            )
        return self._repository.get_by_miembro(id_miembro)
