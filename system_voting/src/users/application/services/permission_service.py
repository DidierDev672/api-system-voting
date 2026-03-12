from typing import List, Optional
from datetime import datetime

from ...domain.entities.permission import (
    UserPermission, 
    CreatePermissionCommand, 
    UpdatePermissionCommand,
    AssignPermissionCommand,
    RevokePermissionCommand
)
from ...domain.value_objects.permissions import Permission, UserRole
from ...domain.ports.permission_repository import PermissionRepositoryPort
from ...domain.ports.user_repository import UserRepositoryPort


class PermissionService:
    """Servicio de Permisos - Application Layer (Hexagonal + Vertical Slicing)"""
    
    def __init__(self, permission_repository: PermissionRepositoryPort, user_repository: UserRepositoryPort):
        self.permission_repository = permission_repository
        self.user_repository = user_repository
    
    def create_user_permissions(self, command: CreatePermissionCommand) -> UserPermission:
        """Crea permisos para un usuario"""
        # Verificar que el usuario existe
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise ValueError(f"Usuario con ID {command.user_id} no encontrado")
        
        # Convertir permisos adicionales de string a enum
        additional_permissions = []
        if command.additional_permissions:
            for perm_str in command.additional_permissions:
                try:
                    additional_permissions.append(Permission(perm_str))
                except ValueError:
                    raise ValueError(f"Permiso no válido: {perm_str}")
        
        # Crear entidad de permisos
        user_permission = UserPermission(
            user_id=command.user_id,
            role=UserRole(command.role),
            assigned_by=command.assigned_by,
            assigned_at=datetime.utcnow(),
            additional_permissions=additional_permissions
        )
        
        # Guardar en repositorio
        return self.permission_repository.save(user_permission)
    
    def get_user_permissions(self, user_id: str) -> Optional[UserPermission]:
        """Obtiene los permisos de un usuario"""
        return self.permission_repository.get_by_user_id(user_id)
    
    def update_user_permissions(self, command: UpdatePermissionCommand) -> UserPermission:
        """Actualiza los permisos de un usuario"""
        # Obtener permisos existentes
        existing_permission = self.permission_repository.get_by_id(command.id)
        if not existing_permission:
            raise ValueError(f"Permisos con ID {command.id} no encontrados")
        
        # Actualizar campos si se proporcionan
        if command.role is not None:
            existing_permission.change_role(command.role)
        
        if command.additional_permissions is not None:
            # Convertir permisos de string a enum
            new_permissions = []
            for perm_str in command.additional_permissions:
                try:
                    new_permissions.append(Permission(perm_str))
                except ValueError:
                    raise ValueError(f"Permiso no válido: {perm_str}")
            existing_permission.additional_permissions = new_permissions
        
        if command.is_active is not None:
            if command.is_active:
                existing_permission.activate()
            else:
                existing_permission.deactivate()
        
        # Guardar cambios
        return self.permission_repository.update(existing_permission)
    
    def assign_additional_permission(self, command: AssignPermissionCommand) -> UserPermission:
        """Asigna un permiso adicional a un usuario"""
        # Obtener permisos existentes del usuario
        user_permission = self.permission_repository.get_by_user_id(command.user_id)
        if not user_permission:
            # Si no tiene permisos registrados, crearlos con rol por defecto
            user_permission = UserPermission(
                user_id=command.user_id,
                role=UserRole("CITIZEN"),
                assigned_by=command.assigned_by,
                assigned_at=datetime.utcnow()
            )
        
        # Convertir string a enum
        try:
            permission = Permission(command.permission)
        except ValueError:
            raise ValueError(f"Permiso no válido: {command.permission}")
        
        # Agregar permiso
        user_permission.add_permission(permission)
        if command.assigned_by:
            user_permission.assigned_by = command.assigned_by
        user_permission.assigned_at = datetime.utcnow()
        
        # Guardar cambios
        return self.permission_repository.save(user_permission)
    
    def revoke_additional_permission(self, command: RevokePermissionCommand) -> UserPermission:
        """Revoca un permiso adicional de un usuario"""
        # Obtener permisos existentes
        user_permission = self.permission_repository.get_by_user_id(command.user_id)
        if not user_permission:
            raise ValueError(f"Usuario {command.user_id} no tiene permisos registrados")
        
        # Convertir string a enum
        try:
            permission = Permission(command.permission)
        except ValueError:
            raise ValueError(f"Permiso no válido: {command.permission}")
        
        # Revocar permiso
        user_permission.remove_permission(permission)
        
        # Guardar cambios
        return self.permission_repository.update(user_permission)
    
    def get_all_permissions(self) -> List[UserPermission]:
        """Obtiene todos los permisos del sistema"""
        return self.permission_repository.get_all()
    
    def get_permissions_by_role(self, role: str) -> List[UserPermission]:
        """Obtiene todos los usuarios con un rol específico"""
        return self.permission_repository.get_by_role(role)
    
    def check_user_permission(self, user_id: str, permission: str) -> bool:
        """Verifica si un usuario tiene un permiso específico"""
        user_permission = self.permission_repository.get_by_user_id(user_id)
        if not user_permission or not user_permission.is_active:
            return False
        
        try:
            perm_enum = Permission(permission)
            return user_permission.has_permission(perm_enum)
        except ValueError:
            return False
    
    def check_user_access(self, user_id: str, required_permissions: List[str]) -> bool:
        """Verifica si un usuario tiene todos los permisos requeridos"""
        user_permission = self.permission_repository.get_by_user_id(user_id)
        if not user_permission or not user_permission.is_active:
            return False
        
        try:
            perm_enums = [Permission(perm) for perm in required_permissions]
            return user_permission.can_access(perm_enums)
        except ValueError:
            return False
    
    def get_available_roles(self) -> List[dict]:
        """Retorna la lista de roles disponibles con sus descripciones"""
        from ...domain.value_objects.permissions import Role
        
        roles_info = []
        for role in Role:
            if role != Role.CITIZEN:  # Excluir rol por defecto de la lista
                roles_info.append({
                    "name": role.value,
                    "display_name": role.value.replace("_", " ").title(),
                    "permissions_count": len(role.permissions),
                    "permissions": [perm.value for perm in role.permissions]
                })
        
        return roles_info
    
    def get_available_permissions(self) -> List[dict]:
        """Retorna la lista de permisos disponibles con sus descripciones"""
        permissions_info = []
        
        # Agrupar permisos por categoría
        categories = {
            "Super Admin": [
                Permission.MANAGE_USERS,
                Permission.MANAGE_SYSTEM,
                Permission.VIEW_ALL_REPORTS,
                Permission.DELETE_ANY_USER,
                Permission.ASSIGN_ROLES
            ],
            "Representante": [
                Permission.MANAGE_GROUP_USERS,
                Permission.VIEW_GROUP_REPORTS,
                Permission.CREATE_VOTING,
                Permission.MANAGE_VOTING
            ],
            "Miembros": [
                Permission.VOTE,
                Permission.VIEW_RESULTS,
                Permission.UPDATE_PROFILE,
                Permission.VIEW_OWN_DATA
            ]
        }
        
        for category, perms in categories.items():
            for perm in perms:
                permissions_info.append({
                    "name": perm.value,
                    "display_name": perm.value.replace("_", " ").title(),
                    "category": category
                })
        
        return permissions_info
