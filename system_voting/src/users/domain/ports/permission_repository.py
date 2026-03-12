from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.entities.permission import UserPermission


class PermissionRepositoryPort(ABC):
    """Puerto del Repositorio de Permisos - Hexagonal Architecture"""
    
    @abstractmethod
    def save(self, user_permission: UserPermission) -> UserPermission:
        """Guarda o actualiza los permisos de un usuario"""
        pass
    
    @abstractmethod
    def get_by_id(self, permission_id: str) -> Optional[UserPermission]:
        """Obtiene permisos por ID"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[UserPermission]:
        """Obtiene permisos por ID de usuario"""
        pass
    
    @abstractmethod
    def get_by_role(self, role: str) -> List[UserPermission]:
        """Obtiene todos los usuarios con un rol específico"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[UserPermission]:
        """Obtiene todos los permisos del sistema"""
        pass
    
    @abstractmethod
    def update(self, user_permission: UserPermission) -> UserPermission:
        """Actualiza los permisos de un usuario"""
        pass
    
    @abstractmethod
    def delete(self, permission_id: str) -> bool:
        """Elimina permisos por ID"""
        pass
    
    @abstractmethod
    def delete_by_user_id(self, user_id: str) -> bool:
        """Elimina permisos por ID de usuario"""
        pass
