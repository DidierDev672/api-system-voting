"""
Repository Port - Screening
Vertical Slicing + SOLID Principles
Interface Segregation, Dependency Inversion
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.screening.domain.entities.screening import (
    Screening,
    CreateScreeningDTO,
)


class ScreeningRepositoryPort(ABC):
    """Abstract port for screening repository"""

    @abstractmethod
    def create(self, screening_data: CreateScreeningDTO) -> Screening:
        """Create a new screening"""
        pass

    @abstractmethod
    def get_all(self) -> List[Screening]:
        """Get all screenings"""
        pass

    @abstractmethod
    def get_by_id(self, screening_id: str) -> Optional[Screening]:
        """Get screening by ID"""
        pass

    @abstractmethod
    def update(self, screening_id: str, screening_data: dict) -> Screening:
        """Update a screening"""
        pass

    @abstractmethod
    def delete(self, screening_id: str) -> bool:
        """Delete a screening"""
        pass
