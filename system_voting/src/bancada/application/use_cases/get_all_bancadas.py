from typing import List
from ...domain.entities.bancada import Bancada
from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class GetAllBancadasUseCase:
    """Caso de uso: Obtener todas las bancadas (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self) -> List[Bancada]:
        return self._repository.get_all()
