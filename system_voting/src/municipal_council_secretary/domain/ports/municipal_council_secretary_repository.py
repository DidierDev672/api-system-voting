"""
Domain Ports - Municipal Council Secretary Repository
Vertical Slicing + SOLID Principles
Interface Segregation, Dependency Inversion
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.municipal_council_secretary.domain.entities.municipal_council_secretary import (
    MunicipalCouncilSecretary,
    CreateMunicipalCouncilSecretaryDTO,
)


class MunicipalCouncilSecretaryRepositoryPort(ABC):
    """Abstract port for municipal council secretary repository"""

    @abstractmethod
    def create(
        self, secretary_data: CreateMunicipalCouncilSecretaryDTO
    ) -> MunicipalCouncilSecretary:
        """Create a new municipal council secretary"""
        pass

    @abstractmethod
    def get_all(self) -> List[MunicipalCouncilSecretary]:
        """Get all municipal council secretaries"""
        pass

    @abstractmethod
    def get_by_id(self, secretary_id: str) -> Optional[MunicipalCouncilSecretary]:
        """Get municipal council secretary by ID"""
        pass

    @abstractmethod
    def get_by_document_id(
        self, document_id: str
    ) -> Optional[MunicipalCouncilSecretary]:
        """Get municipal council secretary by document ID"""
        pass

    @abstractmethod
    def update(
        self, secretary_id: str, secretary_data: dict
    ) -> MunicipalCouncilSecretary:
        """Update a municipal council secretary"""
        pass

    @abstractmethod
    def delete(self, secretary_id: str) -> bool:
        """Delete a municipal council secretary"""
        pass
