from ...domain.entities.bancada import Bancada
from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class UpdateBancadaUseCase:
    """Caso de uso: Actualizar bancada (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self, id: str, bancada: Bancada) -> Bancada:
        if not id or len(id) != 36:
            raise ValueError("El ID debe ser un UUID válido (36 caracteres)")
        bancada.validate()
        return self._repository.update(id, bancada)
