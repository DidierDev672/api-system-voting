from ...domain.ports.bancada_repository import BancadaRepositoryInterface


class DeleteBancadaUseCase:
    """Caso de uso: Eliminar bancada (SRP)"""

    def __init__(self, repository: BancadaRepositoryInterface):
        self._repository = repository

    def execute(self, id: str) -> bool:
        if not id or len(id) != 36:
            raise ValueError("El ID debe ser un UUID válido (36 caracteres)")
        return self._repository.delete(id)
