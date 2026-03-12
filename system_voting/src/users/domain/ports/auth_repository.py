from abc import ABC, abstractmethod
from typing import Optional

from ..entities.auth import AuthToken, AuthenticatedUser, LoginCredentials


class AuthRepositoryPort(ABC):
    """Puerto del Repositorio de Autenticación - Hexagonal Architecture"""
    
    @abstractmethod
    def authenticate(self, credentials: LoginCredentials) -> Optional[AuthenticatedUser]:
        """Autentica un usuario con email y contraseña"""
        pass
    
    @abstractmethod
    def generate_tokens(self, user: AuthenticatedUser) -> AuthToken:
        """Genera tokens de acceso y refresh para un usuario"""
        pass
    
    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> Optional[AuthToken]:
        """Refresca el access token usando el refresh token"""
        pass
    
    @abstractmethod
    def revoke_token(self, refresh_token: str) -> bool:
        """Revoca un refresh token"""
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> Optional[AuthenticatedUser]:
        """Valida un token y retorna el usuario autenticado"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[AuthenticatedUser]:
        """Obtiene un usuario autenticado por ID"""
        pass
    
    @abstractmethod
    def update_last_login(self, user_id: str) -> bool:
        """Actualiza la fecha de último login del usuario"""
        pass
    
    @abstractmethod
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Cambia la contraseña de un usuario"""
        pass
    
    @abstractmethod
    def reset_password(self, email: str) -> bool:
        """Inicia el proceso de reseteo de contraseña"""
        pass
