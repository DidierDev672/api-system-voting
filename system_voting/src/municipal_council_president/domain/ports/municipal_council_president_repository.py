"""
Domain Ports - Municipal Council President Repository
Vertical Slicing + SOLID Principles
Interface Segregation, Dependency Inversion
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.municipal_council_president.domain.entities.municipal_council_president import (
    MunicipalCouncilPresident,
    CreateMunicipalCouncilPresidentDTO,
)


class MunicipalCouncilPresidentRepositoryPort(ABC):
    """Abstract port for municipal council president repository"""

    @abstractmethod
    def create(
        self, president_data: CreateMunicipalCouncilPresidentDTO
    ) -> MunicipalCouncilPresident:
        """Create a new municipal council president"""
        pass

    @abstractmethod
    def get_all(self) -> List[MunicipalCouncilPresident]:
        """Get all municipal council presidents"""
        pass

    @abstractmethod
    def get_by_id(self, president_id: str) -> Optional[MunicipalCouncilPresident]:
        """Get municipal council president by ID"""
        pass

    @abstractmethod
    def get_by_document_id(
        self, document_id: str
    ) -> Optional[MunicipalCouncilPresident]:
        """Get municipal council president by document ID"""
        pass

    @abstractmethod
    def update(
        self, president_id: str, president_data: dict
    ) -> MunicipalCouncilPresident:
        """Update a municipal council president"""
        pass

    @abstractmethod
    def delete(self, president_id: str) -> bool:
        """Delete a municipal council president"""
        pass
