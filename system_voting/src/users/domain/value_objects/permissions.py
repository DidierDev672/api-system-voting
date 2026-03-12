from enum import Enum
from typing import List, Set


class Permission(Enum):
    """Enum de permisos del sistema - Vertical Slicing + Hexagonal"""
    
    # Permisos de Super Admin
    MANAGE_USERS = "manage_users"
    MANAGE_SYSTEM = "manage_system"
    VIEW_ALL_REPORTS = "view_all_reports"
    DELETE_ANY_USER = "delete_any_user"
    ASSIGN_ROLES = "assign_roles"
    
    # Permisos de Representante
    MANAGE_GROUP_USERS = "manage_group_users"
    VIEW_GROUP_REPORTS = "view_group_reports"
    CREATE_VOTING = "create_voting"
    MANAGE_VOTING = "manage_voting"
    
    # Permisos de Miembros
    VOTE = "vote"
    VIEW_RESULTS = "view_results"
    UPDATE_PROFILE = "update_profile"
    VIEW_OWN_DATA = "view_own_data"


class Role(Enum):
    """Roles del sistema con sus permisos asociados"""
    
    SUPER_ADMIN = "SUPER_ADMIN"
    REPRESENTATIVE = "REPRESENTATIVE" 
    MEMBER = "MEMBER"
    CITIZEN = "CITIZEN"  # Rol por defecto
    
    # Mapeo a valores que espera la base de datos
    @classmethod
    def get_valid_roles(cls):
        """Retorna los roles válidos según la base de datos"""
        return ["SUPER_ADMIN", "REPRESENTATIVE", "MEMBER", "CITIZEN"]
    
    @classmethod
    def validate_role(cls, role: str) -> str:
        """Valida y retorna un rol válido según restricciones de la base de datos"""
        valid_roles = cls.get_valid_roles()
        
        # Mapeo de roles problemáticos a valores aceptados
        role_mapping = {
            "MEMBER": "CITIZEN",  # Si MEMBER no es aceptado, usar CITIZEN
            "REPRESENTATIVE": "REPRESENTATIVE",
            "SUPER_ADMIN": "SUPER_ADMIN", 
            "CITIZEN": "CITIZEN"
        }
        
        upper_role = role.upper()
        if upper_role in role_mapping:
            mapped_role = role_mapping[upper_role]
            if mapped_role != upper_role:
                print(f"Rol '{role}' mapeado a '{mapped_role}' por restricciones de base de datos")
            return mapped_role
        
        # Si no coincide con ningún rol conocido, usar CITIZEN como fallback
        return "CITIZEN"
    
    @property
    def permissions(self) -> Set[Permission]:
        """Retorna los permisos asociados a cada rol"""
        if self == Role.SUPER_ADMIN:
            return {
                Permission.MANAGE_USERS,
                Permission.MANAGE_SYSTEM,
                Permission.VIEW_ALL_REPORTS,
                Permission.DELETE_ANY_USER,
                Permission.ASSIGN_ROLES,
                # Hereda permisos de roles inferiores
                Permission.MANAGE_GROUP_USERS,
                Permission.VIEW_GROUP_REPORTS,
                Permission.CREATE_VOTING,
                Permission.MANAGE_VOTING,
                Permission.VOTE,
                Permission.VIEW_RESULTS,
                Permission.UPDATE_PROFILE,
                Permission.VIEW_OWN_DATA
            }
        
        elif self == Role.REPRESENTATIVE:
            return {
                Permission.MANAGE_GROUP_USERS,
                Permission.VIEW_GROUP_REPORTS,
                Permission.CREATE_VOTING,
                Permission.MANAGE_VOTING,
                # Hereda permisos de miembros
                Permission.VOTE,
                Permission.VIEW_RESULTS,
                Permission.UPDATE_PROFILE,
                Permission.VIEW_OWN_DATA
            }
        
        elif self == Role.MEMBER:
            return {
                Permission.VOTE,
                Permission.VIEW_RESULTS,
                Permission.UPDATE_PROFILE,
                Permission.VIEW_OWN_DATA
            }
        
        elif self == Role.CITIZEN:
            return {
                Permission.UPDATE_PROFILE,
                Permission.VIEW_OWN_DATA
            }
        
        return set()
    
    def has_permission(self, permission: Permission) -> bool:
        """Verifica si el rol tiene un permiso específico"""
        return permission in self.permissions
    
    def can_access(self, required_permissions: List[Permission]) -> bool:
        """Verifica si el rol tiene todos los permisos requeridos"""
        return all(perm in self.permissions for perm in required_permissions)


class UserRole:
    """Value Object para manejo de roles y permisos de usuario"""
    
    def __init__(self, role: str):
        self.role = Role(role.upper()) if role else Role.CITIZEN
    
    @property
    def role_enum(self) -> Role:
        return self.role
    
    @property
    def role_name(self) -> str:
        return self.role.value
    
    @property
    def permissions(self) -> Set[Permission]:
        return self.role.permissions
    
    def has_permission(self, permission: Permission) -> bool:
        return self.role.has_permission(permission)
    
    def can_access(self, required_permissions: List[Permission]) -> bool:
        return self.role.can_access(required_permissions)
    
    def change_role(self, new_role: str):
        """Cambia el rol del usuario"""
        self.role = Role(new_role.upper())
    
    def __str__(self) -> str:
        return self.role.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, UserRole):
            return self.role == other.role
        return False
