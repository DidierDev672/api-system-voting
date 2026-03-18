from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.bancada import Bancada


class BancadaRepositoryInterface(ABC):
    """Port - Interfaz para el repositorio de bancada (ISP)"""

    @abstractmethod
    def get_all(self) -> List[Bancada]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Bancada]:
        pass

    @abstractmethod
    def get_by_miembro(self, id_miembro: str) -> List[Bancada]:
        pass

    @abstractmethod
    def get_by_partido(self, id_partido: str) -> List[Bancada]:
        pass

    @abstractmethod
    def create(self, bancada: Bancada) -> Bancada:
        pass

    @abstractmethod
    def update(self, id: str, bancada: Bancada) -> Bancada:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
