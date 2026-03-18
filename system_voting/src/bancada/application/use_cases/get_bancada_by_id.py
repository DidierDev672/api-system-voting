from typing import Optional
from ...domain.entities.bancada import Bancada
from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class GetBancadaByIdUseCase:
    """Caso de uso: Obtener bancada por ID (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self, id: str) -> Optional[Bancada]:
        if not id or len(id) != 36:
            raise ValueError("El ID debe ser un UUID válido (36 caracteres)")
        return self._repository.get_by_id(id)
