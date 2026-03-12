from abc import ABC, abstractmethod
from typing import Optional, List
from system_voting.src.users.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

class UserRepositoryPort(ABC):
    """Puerto del Repositorio de Usuarios - Hexagonal Architecture"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda o actualiza un usuario"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        pass
    
    @abstractmethod
    def get_by_document(self, document_type: str, document_number: str) -> Optional[User]:
        """Obtiene un usuario por tipo y número de documento"""
        pass
    
    @abstractmethod
    def get_all(self, active_only: bool = True) -> List[User]:
        """Obtiene todos los usuarios"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Elimina un usuario por ID"""
        pass