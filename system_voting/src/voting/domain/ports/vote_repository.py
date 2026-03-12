"""
Puerto de Salida para Votos - Interfaz Hexagonal
Vertical Slicing + Hexagonal Architecture
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.voting.domain.entities.vote import Vote


class VoteRepositoryPort(ABC):
    """Puerto abstracto para el repositorio de votos"""

    @abstractmethod
    def save(self, vote: Vote) -> Vote:
        """Persistir un nuevo voto"""
        pass

    @abstractmethod
    def find_by_id(self, vote_id: str) -> Optional[Vote]:
        """Obtener voto por ID"""
        pass

    @abstractmethod
    def find_by_consultation(self, id_consult: str) -> List[Vote]:
        """Obtener todos los votos de una consulta"""
        pass

    @abstractmethod
    def find_by_member(self, id_member: str) -> List[Vote]:
        """Obtener todos los votos de un miembro"""
        pass

    @abstractmethod
    def exists_by_member_and_consult(self, id_member: str, id_consult: str) -> bool:
        """Verificar si un miembro ya votó en una consulta"""
        pass

    @abstractmethod
    def delete(self, vote_id: str) -> bool:
        """Eliminar un voto"""
        pass
