from abc import ABC, abstractmethod
from typing import List, Optional
from system_voting.src.users.domain.entities.user import User


class UserRepository(ABC):
    """Puerto (Repository) - Arquitectura Hexagonal"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Guardar un nuevo usuario"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        pass
    
    @abstractmethod
    def get_by_document(self, document_type: str, document_number: str) -> Optional[User]:
        """Obtener usuario por documento"""
        pass
    
    @abstractmethod
    def get_all(self, active_only: bool = True) -> List[User]:
        """Obtener todos los usuarios"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Actualizar un usuario"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Eliminar un usuario (soft delete)"""
        pass
