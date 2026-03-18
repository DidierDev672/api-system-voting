from ...domain.entities.bancada import Bancada
from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class CreateBancadaUseCase:
    """Caso de uso: Crear nueva bancada (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self, bancada: Bancada) -> Bancada:
        bancada.validate()
        return self._repository.create(bancada)
