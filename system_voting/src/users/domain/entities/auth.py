from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta


@dataclass
class AuthToken:
    """Entidad de Token de Autenticación - Dominio Puro (Vertical Slicing + Hexagonal)"""
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600  # 1 hora por defecto
    issued_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones de dominio - Lógica de negocio pura"""
        if not self.access_token:
            raise ValueError("El access token es obligatorio")
        
        if not self.refresh_token:
            raise ValueError("El refresh token es obligatorio")
        
        if self.issued_at is None:
            self.issued_at = datetime.utcnow()
    
    @property
    def expires_at(self) -> datetime:
        """Retorna la fecha de expiración del token"""
        return self.issued_at + timedelta(seconds=self.expires_in)
    
    def is_expired(self) -> bool:
        """Verifica si el token ha expirado"""
        return datetime.utcnow() > self.expires_at
    
    def is_expiring_soon(self, minutes: int = 5) -> bool:
        """Verifica si el token expirará pronto"""
        soon = datetime.utcnow() + timedelta(minutes=minutes)
        return self.expires_at <= soon


@dataclass
class LoginCredentials:
    """Entidad de Credenciales de Login - Dominio Puro"""
    email: str
    password: str
    
    def __post_init__(self):
        """Validaciones de dominio - Lógica de negocio pura"""
        if not self.email or "@" not in self.email:
            raise ValueError("El correo electrónico no es válido")
        
        if not self.password or len(self.password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")


@dataclass
class AuthenticatedUser:
    """Entidad de Usuario Autenticado - Dominio Puro"""
    id: str
    email: str
    full_name: str
    role: str
    permissions: list
    is_active: bool = True
    last_login: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones de dominio - Lógica de negocio pura"""
        if not self.id:
            raise ValueError("El ID del usuario es obligatorio")
        
        if not self.email:
            raise ValueError("El correo electrónico es obligatorio")
        
        if not self.full_name:
            raise ValueError("El nombre completo es obligatorio")
        
        if not self.role:
            raise ValueError("El rol del usuario es obligatorio")
        
        if self.permissions is None:
            self.permissions = []
        
        if self.last_login is None:
            self.last_login = datetime.utcnow()
    
    def has_permission(self, permission: str) -> bool:
        """Verifica si el usuario tiene un permiso específico"""
        return permission in self.permissions
    
    def has_any_permission(self, permissions: list) -> bool:
        """Verifica si el usuario tiene al menos uno de los permisos"""
        return any(perm in self.permissions for perm in permissions)
    
    def has_all_permissions(self, permissions: list) -> bool:
        """Verifica si el usuario tiene todos los permisos requeridos"""
        return all(perm in self.permissions for perm in permissions)


@dataclass
class LoginCommand:
    """Comando para login - Application Layer (Hexagonal)"""
    email: str
    password: str


@dataclass
class RegisterCommand:
    """Comando para registro con autenticación - Application Layer"""
    full_name: str
    document_type: str
    document_number: str
    email: str
    password: str
    phone: Optional[str] = None
    role: str = "CITIZEN"


@dataclass
class RefreshTokenCommand:
    """Comando para refresh token - Application Layer"""
    refresh_token: str


@dataclass
class LogoutCommand:
    """Comando para logout - Application Layer"""
    refresh_token: str
    user_id: str


@dataclass
class ChangePasswordCommand:
    """Comando para cambio de contraseña - Application Layer"""
    user_id: str
    current_password: str
    new_password: str


@dataclass
class ResetPasswordCommand:
    """Comando para reseteo de contraseña - Application Layer"""
    email: str
