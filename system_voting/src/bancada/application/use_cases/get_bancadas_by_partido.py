from typing import List
from ...domain.entities.bancada import Bancada
from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class GetBancadasByPartidoUseCase:
    """Caso de uso: Obtener bancadas por partido (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self, id_partido: str) -> List[Bancada]:
        if not id_partido or len(id_partido) != 36:
            raise ValueError(
                "El ID del partido debe ser un UUID válido (36 caracteres)"
            )
        return self._repository.get_by_partido(id_partido)
