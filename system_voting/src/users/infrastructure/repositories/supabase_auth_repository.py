import hashlib
from datetime import datetime
from typing import Optional

from ...domain.entities.auth import (
    AuthToken, 
    AuthenticatedUser, 
    LoginCredentials
)
from ...domain.ports.auth_repository import AuthRepositoryPort
from ...domain.ports.user_repository import UserRepositoryPort
from ...domain.ports.permission_repository import PermissionRepositoryPort
from ...application.services.auth_service import JWTTokenService


class SupabaseAuthRepository(AuthRepositoryPort):
    """Implementación del repositorio de autenticación con Supabase - Hexagonal Architecture"""
    
    def __init__(self, 
                 user_repository: UserRepositoryPort,
                 permission_repository: PermissionRepositoryPort):
        self.user_repository = user_repository
        self.permission_repository = permission_repository
        self.jwt_service = JWTTokenService()
        
        # Simulación de tokens revocados (en producción, usar Redis o base de datos)
        self._revoked_tokens = set()
    
    def authenticate(self, credentials: LoginCredentials) -> Optional[AuthenticatedUser]:
        """Autentica un usuario con email y contraseña"""
        # Buscar usuario por email
        user = self.user_repository.get_by_email(credentials.email)
        if not user:
            return None
        
        # Verificar contraseña
        if not self._verify_password(credentials.password, user.password or ""):
            return None
        
        # Verificar si está activo
        if not user.is_active:
            return None
        
        # Crear usuario autenticado con permisos
        return self._create_authenticated_user(user)
    
    def generate_tokens(self, user: AuthenticatedUser) -> AuthToken:
        """Genera tokens de acceso y refresh para un usuario"""
        return self.jwt_service.generate_tokens(user)
    
    def refresh_access_token(self, refresh_token: str) -> Optional[AuthToken]:
        """Refresca el access token usando el refresh token"""
        # Validar refresh token
        payload = self.jwt_service.validate_refresh_token(refresh_token)
        if not payload:
            return None
        
        # Verificar que no esté revocado
        if refresh_token in self._revoked_tokens:
            return None
        
        # Obtener usuario
        user = self.get_user_by_id(payload['user_id'])
        if not user or not user.is_active:
            return None
        
        # Generar nuevos tokens
        return self.jwt_service.generate_tokens(user)
    
    def revoke_token(self, refresh_token: str) -> bool:
        """Revoca un refresh token"""
        try:
            # Validar el token antes de revocar
            payload = self.jwt_service.validate_refresh_token(refresh_token)
            if payload:
                self._revoked_tokens.add(refresh_token)
                return True
        except Exception:
            pass
        
        return False
    
    def validate_token(self, token: str) -> Optional[AuthenticatedUser]:
        """Valida un token y retorna el usuario autenticado"""
        # Validar access token
        payload = self.jwt_service.validate_access_token(token)
        if not payload:
            return None
        
        # Obtener usuario
        user = self.get_user_by_id(payload['user_id'])
        if not user or not user.is_active:
            return None
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        """Obtiene un usuario autenticado por ID"""
        # Buscar usuario
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        # Crear usuario autenticado con permisos
        return self._create_authenticated_user(user)
    
    def update_last_login(self, user_id: str) -> bool:
        """Actualiza la fecha de último login del usuario"""
        try:
            user = self.user_repository.get_by_id(user_id)
            if user:
                # En una implementación real, esto actualizaría la base de datos
                # Por ahora, simulamos que se actualiza correctamente
                return True
        except Exception:
            pass
        
        return False
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Cambia la contraseña de un usuario"""
        try:
            user = self.user_repository.get_by_id(user_id)
            if not user:
                return False
            
            # Verificar contraseña actual
            if not self._verify_password(current_password, user.password or ""):
                return False
            
            # Hashear nueva contraseña
            hashed_new_password = self._hash_password(new_password)
            
            # Actualizar contraseña
            user.password = hashed_new_password
            self.user_repository.update(user)
            
            return True
        except Exception:
            pass
        
        return False
    
    def reset_password(self, email: str) -> bool:
        """Inicia el proceso de reseteo de contraseña"""
        try:
            user = self.user_repository.get_by_email(email)
            if not user:
                return False
            
            # En una implementación real, esto enviaría un email con un token de reset
            # Por ahora, simulamos que se envía correctamente
            print(f"Email de reseteo enviado a {email}")
            return True
        except Exception:
            pass
        
        return False
    
    def _create_authenticated_user(self, user) -> AuthenticatedUser:
        """Crea un AuthenticatedUser a partir de un User"""
        # Obtener permisos del usuario
        user_permission = self.permission_repository.get_by_user_id(user.id)
        permissions = []
        
        if user_permission and user_permission.is_active:
            permissions = [perm.value for perm in user_permission.get_all_permissions()]
        
        return AuthenticatedUser(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            permissions=permissions,
            is_active=user.is_active
        )
    
    def _hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica una contraseña hasheada"""
        return self._hash_password(password) == hashed_password
