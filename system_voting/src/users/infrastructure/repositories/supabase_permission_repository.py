from typing import List, Optional
import json
from datetime import datetime

from ...domain.entities.permission import UserPermission
from ...domain.value_objects.permissions import Permission, UserRole
from ...domain.ports.permission_repository import PermissionRepositoryPort


class SupabasePermissionRepository(PermissionRepositoryPort):
    """Implementación del repositorio de permisos con Supabase - Hexagonal Architecture"""
    
    def __init__(self):
        # Aquí iría la configuración del cliente de Supabase
        # Por ahora, usaremos una simulación para demostrar la estructura
        self._permissions_db = {}  # Simulación de base de datos
    
    def _serialize_permission(self, user_permission: UserPermission) -> dict:
        """Serializa la entidad de permisos a formato de base de datos"""
        return {
            "id": user_permission.id,
            "user_id": user_permission.user_id,
            "role": user_permission.role.role_name,
            "assigned_by": user_permission.assigned_by,
            "assigned_at": user_permission.assigned_at.isoformat() if user_permission.assigned_at else None,
            "is_active": user_permission.is_active,
            "additional_permissions": [perm.value for perm in user_permission.additional_permissions],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def _deserialize_permission(self, data: dict) -> UserPermission:
        """Deserializa los datos de la base de datos a entidad de permisos"""
        additional_permissions = []
        if data.get("additional_permissions"):
            additional_permissions = [Permission(perm) for perm in data["additional_permissions"]]
        
        return UserPermission(
            id=data.get("id"),
            user_id=data["user_id"],
            role=UserRole(data["role"]),
            assigned_by=data.get("assigned_by"),
            assigned_at=datetime.fromisoformat(data["assigned_at"]) if data.get("assigned_at") else None,
            is_active=data.get("is_active", True),
            additional_permissions=additional_permissions
        )
    
    def save(self, user_permission: UserPermission) -> UserPermission:
        """Guarda o actualiza los permisos de un usuario"""
        if not user_permission.id:
            # Generar ID único (en producción, usar UUID de la base de datos)
            import uuid
            user_permission.id = str(uuid.uuid4())
        
        # Serializar y guardar
        permission_data = self._serialize_permission(user_permission)
        self._permissions_db[user_permission.id] = permission_data
        
        return user_permission
    
    def get_by_id(self, permission_id: str) -> Optional[UserPermission]:
        """Obtiene permisos por ID"""
        permission_data = self._permissions_db.get(permission_id)
        if permission_data:
            return self._deserialize_permission(permission_data)
        return None
    
    def get_by_user_id(self, user_id: str) -> Optional[UserPermission]:
        """Obtiene permisos por ID de usuario"""
        for permission_data in self._permissions_db.values():
            if permission_data["user_id"] == user_id:
                return self._deserialize_permission(permission_data)
        return None
    
    def get_by_role(self, role: str) -> List[UserPermission]:
        """Obtiene todos los usuarios con un rol específico"""
        result = []
        for permission_data in self._permissions_db.values():
            if permission_data["role"] == role.upper():
                result.append(self._deserialize_permission(permission_data))
        return result
    
    def get_all(self) -> List[UserPermission]:
        """Obtiene todos los permisos del sistema"""
        result = []
        for permission_data in self._permissions_db.values():
            result.append(self._deserialize_permission(permission_data))
        return result
    
    def update(self, user_permission: UserPermission) -> UserPermission:
        """Actualiza los permisos de un usuario"""
        if not user_permission.id:
            raise ValueError("No se puede actualizar permisos sin ID")
        
        permission_data = self._serialize_permission(user_permission)
        permission_data["updated_at"] = datetime.utcnow().isoformat()
        self._permissions_db[user_permission.id] = permission_data
        
        return user_permission
    
    def delete(self, permission_id: str) -> bool:
        """Elimina permisos por ID"""
        if permission_id in self._permissions_db:
            del self._permissions_db[permission_id]
            return True
        return False
    
    def delete_by_user_id(self, user_id: str) -> bool:
        """Elimina permisos por ID de usuario"""
        to_delete = []
        for perm_id, permission_data in self._permissions_db.items():
            if permission_data["user_id"] == user_id:
                to_delete.append(perm_id)
        
        for perm_id in to_delete:
            del self._permissions_db[perm_id]
        
        return len(to_delete) > 0
