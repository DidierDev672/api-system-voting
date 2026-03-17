"""
Domain Ports - Municipal Council Session Repository
Vertical Slicing + SOLID Principles
Interface Segregation, Dependency Inversion
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.municipal_council_session.domain.entities.municipal_council_session import (
    MunicipalCouncilSession,
    CreateMunicipalCouncilSessionDTO,
)


class MunicipalCouncilSessionRepositoryPort(ABC):
    """Abstract port for municipal council session repository"""

    @abstractmethod
    def create(
        self, session_data: CreateMunicipalCouncilSessionDTO
    ) -> MunicipalCouncilSession:
        """Create a new municipal council session"""
        pass

    @abstractmethod
    def get_all(self) -> List[MunicipalCouncilSession]:
        """Get all municipal council sessions"""
        pass

    @abstractmethod
    def get_by_id(self, session_id: str) -> Optional[MunicipalCouncilSession]:
        """Get municipal council session by ID"""
        pass

    @abstractmethod
    def update(self, session_id: str, session_data: dict) -> MunicipalCouncilSession:
        """Update a municipal council session"""
        pass

    @abstractmethod
    def delete(self, session_id: str) -> bool:
        """Delete a municipal council session"""
        pass
