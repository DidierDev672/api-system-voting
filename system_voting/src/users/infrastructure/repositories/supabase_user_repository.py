from typing import List, Optional, Dict, Any
from supabase_integration import users_service as users_svc
from system_voting.src.users.domain.entities.user import User
from system_voting.src.users.domain.ports.user_repository import UserRepositoryPort


class SupabaseUserRepository(UserRepositoryPort):
    """Adaptador - Implementación del puerto con Supabase (Hexagonal)"""

    def __init__(self):
        self.supabase_service = users_svc

    def save(self, user: User) -> User:
        """Guardar un nuevo usuario en Supabase"""
        user_data = {
            "auth_id": user.auth_id,
            "full_name": user.full_name,
            "document_type": user.document_type,
            "document_number": user.document_number,
            "email": user.email,
            "phone": user.phone,
            "password": user.password,
            "role": user.role,
            "is_active": user.is_active,
        }

        result = self.supabase_service.create_user(user_data)
        return self._map_to_entity(result)

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtener usuario por ID desde Supabase"""
        result = self.supabase_service.get_user_by_id(user_id)
        if not result:
            return None
        return self._map_to_entity(result)

    def get_by_auth_id(self, auth_id: str) -> Optional[User]:
        """Obtener usuario por auth_id de Supabase"""
        result = self.supabase_service.get_user_by_auth_id(auth_id)
        if not result:
            return None
        return self._map_to_entity(result)

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email desde Supabase"""
        result = self.supabase_service.get_user_by_email(email)
        if not result:
            return None
        return self._map_to_entity(result)

    def get_by_document(
        self, document_type: str, document_number: str
    ) -> Optional[User]:
        """Obtener usuario por documento desde Supabase"""
        result = self.supabase_service.get_user_by_document(
            document_type, document_number
        )
        if not result:
            return None
        return self._map_to_entity(result)

    def get_all(self, active_only: bool = True) -> List[User]:
        """Obtener todos los usuarios desde Supabase"""
        results = self.supabase_service.get_all_users(active_only)
        return [self._map_to_entity(result) for result in results]

    def update(self, user: User) -> User:
        """Actualizar usuario en Supabase"""
        user_data = {
            "full_name": user.full_name,
            "document_type": user.document_type,
            "document_number": user.document_number,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_active": user.is_active,
        }

        result = self.supabase_service.update_user(user.id, user_data)
        return self._map_to_entity(result)

    def update_by_auth_id(self, auth_id: str, user_data: Dict[str, Any]) -> User:
        """Actualizar usuario por auth_id"""
        result = self.supabase_service.update_user_by_auth_id(auth_id, user_data)
        return self._map_to_entity(result)

    def delete(self, user_id: str) -> bool:
        """Eliminar usuario (soft delete) en Supabase"""
        return self.supabase_service.delete_user(user_id)

    def _map_to_entity(self, data: Dict[str, Any]) -> User:
        """Mapear datos de Supabase a entidad de dominio"""
        return User(
            id=data.get("id"),
            auth_id=data.get("auth_id"),
            full_name=data.get("full_name", ""),
            document_type=data.get("document_type", ""),
            document_number=data.get("document_number", ""),
            email=data.get("email", ""),
            password=data.get("password"),
            phone=data.get("phone"),
            role=data.get("role", "CITIZEN"),
            is_active=data.get("is_active", True),
        )
