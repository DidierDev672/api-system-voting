"""
Repository Port - Alcaldia
Domain Layer
Dependency Inversion Principle - Interface for infrastructure
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.alcaldia.domain.entities.alcaldia import (
    Alcaldia,
    CreateAlcaldiaDTO,
    UpdateAlcaldiaDTO,
)


class AlcaldiaRepositoryPort(ABC):
    """Port interface for Alcaldia repository"""

    @abstractmethod
    def create(self, data: CreateAlcaldiaDTO) -> Alcaldia:
        """Create a new alcaldia"""
        pass

    @abstractmethod
    def get_all(self) -> List[Alcaldia]:
        """Get all alcaldias"""
        pass

    @abstractmethod
    def get_by_id(self, alcaldia_id: str) -> Optional[Alcaldia]:
        """Get alcaldia by ID"""
        pass

    @abstractmethod
    def update(self, alcaldia_id: str, data: UpdateAlcaldiaDTO) -> Alcaldia:
        """Update an alcaldia"""
        pass

    @abstractmethod
    def delete(self, alcaldia_id: str) -> bool:
        """Delete an alcaldia"""
        pass
