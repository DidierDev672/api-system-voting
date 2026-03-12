from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..value_objects.permissions import UserRole, Permission, Role


@dataclass
class UserPermission:
    """Entidad de Permisos de Usuario - Dominio Puro (Vertical Slicing + Hexagonal)"""
    id: Optional[str] = None
    user_id: str = ""
    role: UserRole = None
    assigned_by: Optional[str] = None
    assigned_at: Optional[datetime] = None
    is_active: bool = True
    additional_permissions: List[Permission] = None
    
    def __post_init__(self):
        """Validaciones de dominio - Lógica de negocio pura"""
        if not self.user_id:
            raise ValueError("El ID del usuario es obligatorio")
        
        if self.role is None:
            self.role = UserRole("CITIZEN")
        
        if self.additional_permissions is None:
            self.additional_permissions = []
        
        if self.assigned_at is None:
            self.assigned_at = datetime.utcnow()
    
    def get_all_permissions(self) -> List[Permission]:
        """Retorna todos los permisos del usuario (rol + adicionales)"""
        role_permissions = list(self.role.permissions)
        return list(set(role_permissions + self.additional_permissions))
    
    def has_permission(self, permission: Permission) -> bool:
        """Verifica si el usuario tiene un permiso específico"""
        return self.role.has_permission(permission) or permission in self.additional_permissions
    
    def can_access(self, required_permissions: List[Permission]) -> bool:
        """Verifica si el usuario tiene todos los permisos requeridos"""
        return all(perm in self.get_all_permissions() for perm in required_permissions)
    
    def add_permission(self, permission: Permission):
        """Agrega un permiso adicional al usuario"""
        if permission not in self.additional_permissions:
            self.additional_permissions.append(permission)
    
    def remove_permission(self, permission: Permission):
        """Remueve un permiso adicional del usuario"""
        if permission in self.additional_permissions:
            self.additional_permissions.remove(permission)
    
    def change_role(self, new_role: str, assigned_by: Optional[str] = None):
        """Cambia el rol del usuario"""
        self.role = UserRole(new_role)
        if assigned_by:
            self.assigned_by = assigned_by
        self.assigned_at = datetime.utcnow()
    
    def deactivate(self):
        """Desactiva los permisos del usuario"""
        self.is_active = False
    
    def activate(self):
        """Activa los permisos del usuario"""
        self.is_active = True


@dataclass
class CreatePermissionCommand:
    """Comando para crear permisos de usuario - Application Layer (Hexagonal)"""
    user_id: str
    role: str
    assigned_by: Optional[str] = None
    additional_permissions: List[str] = None


@dataclass
class UpdatePermissionCommand:
    """Comando para actualizar permisos de usuario - Application Layer"""
    id: str
    role: Optional[str] = None
    additional_permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None


@dataclass
class AssignPermissionCommand:
    """Comando para asignar permisos adicionales - Application Layer"""
    user_id: str
    permission: str
    assigned_by: Optional[str] = None


@dataclass
class RevokePermissionCommand:
    """Comando para revocar permisos adicionales - Application Layer"""
    user_id: str
    permission: str
