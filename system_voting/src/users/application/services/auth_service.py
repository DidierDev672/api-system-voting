import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings

from ...domain.entities.auth import (
    AuthToken, 
    AuthenticatedUser, 
    LoginCredentials,
    LoginCommand,
    RegisterCommand,
    RefreshTokenCommand,
    LogoutCommand,
    ChangePasswordCommand,
    ResetPasswordCommand
)
from ...domain.ports.auth_repository import AuthRepositoryPort
from ...domain.ports.user_repository import UserRepositoryPort
from ...domain.ports.permission_repository import PermissionRepositoryPort
from ...domain.entities.user import CreateUserCommand, User


class AuthService:
    """Servicio de Autenticación - Application Layer (Hexagonal + Vertical Slicing)"""
    
    def __init__(self, 
                 auth_repository: AuthRepositoryPort,
                 user_repository: UserRepositoryPort,
                 permission_repository: PermissionRepositoryPort):
        self.auth_repository = auth_repository
        self.user_repository = user_repository
        self.permission_repository = permission_repository
    
    def login(self, command: LoginCommand) -> tuple[AuthenticatedUser, AuthToken]:
        """Autentica un usuario y genera tokens"""
        # Crear credenciales
        credentials = LoginCredentials(
            email=command.email,
            password=command.password
        )
        
        # Autenticar usuario
        user = self.auth_repository.authenticate(credentials)
        if not user:
            raise ValueError("Credenciales inválidas")
        
        if not user.is_active:
            raise ValueError("Usuario inactivo")
        
        # Generar tokens
        tokens = self.auth_repository.generate_tokens(user)
        
        # Actualizar último login
        self.auth_repository.update_last_login(user.id)
        
        return user, tokens
    
    def register(self, command: RegisterCommand) -> tuple[AuthenticatedUser, AuthToken]:
        """Registra un nuevo usuario y genera tokens"""
        # Verificar si el usuario ya existe
        existing_user = self.user_repository.get_by_email(command.email)
        if existing_user:
            raise ValueError("El correo electrónico ya está registrado")
        
        # Verificar si el documento ya existe
        existing_document = self.user_repository.get_by_document(command.document_type, command.document_number)
        if existing_document:
            raise ValueError("El número de documento ya está registrado")
        
        # Hashear contraseña
        hashed_password = self._hash_password(command.password)
        
        # Validar roles permitidos
        from ...domain.value_objects.permissions import Role
        valid_roles = Role.get_valid_roles()
        role = Role.validate_role(command.role)
        if role != command.role:
            # Si el rol fue ajustado, informar al usuario
            print(f"Rol ajustado de '{command.role}' a '{role}' por restricciones de la base de datos")
        
        # Crear comando de usuario
        create_command = CreateUserCommand(
            full_name=command.full_name,
            document_type=command.document_type,
            document_number=command.document_number,
            email=command.email,
            password=hashed_password,
            phone=command.phone,
            role=role
        )
        
        # Crear usuario
        user = self.user_repository.save(User(
            full_name=create_command.full_name,
            document_type=create_command.document_type,
            document_number=create_command.document_number,
            email=create_command.email,
            password=create_command.password,
            phone=create_command.phone,
            role=create_command.role
        ))
        
        # Crear permisos por defecto
        from ...application.services.permission_service import PermissionService
        permission_service = PermissionService(self.permission_repository, self.user_repository)
        from ...domain.entities.permission import CreatePermissionCommand
        
        permission_service.create_user_permissions(CreatePermissionCommand(
            user_id=user.id,
            role=command.role
        ))
        
        # Autenticar y generar tokens
        authenticated_user = self._create_authenticated_user(user)
        tokens = self.auth_repository.generate_tokens(authenticated_user)
        
        return authenticated_user, tokens
    
    def refresh_token(self, command: RefreshTokenCommand) -> AuthToken:
        """Refresca el access token"""
        tokens = self.auth_repository.refresh_access_token(command.refresh_token)
        if not tokens:
            raise ValueError("Refresh token inválido o expirado")
        
        return tokens
    
    def logout(self, command: LogoutCommand) -> bool:
        """Cierra sesión del usuario revocando el token"""
        return self.auth_repository.revoke_token(command.refresh_token)
    
    def get_current_user(self, token: str) -> Optional[AuthenticatedUser]:
        """Obtiene el usuario actual a partir del token"""
        return self.auth_repository.validate_token(token)
    
    def change_password(self, command: ChangePasswordCommand) -> bool:
        """Cambia la contraseña de un usuario"""
        # Verificar contraseña actual
        user = self.user_repository.get_by_id(command.user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        
        if not self._verify_password(command.current_password, user.password or ""):
            raise ValueError("Contraseña actual incorrecta")
        
        # Hashear nueva contraseña
        new_hashed_password = self._hash_password(command.new_password)
        
        # Cambiar contraseña
        return self.auth_repository.change_password(
            command.user_id, 
            command.current_password, 
            new_hashed_password
        )
    
    def reset_password(self, command: ResetPasswordCommand) -> bool:
        """Inicia el proceso de reseteo de contraseña"""
        return self.auth_repository.reset_password(command.email)
    
    def _create_authenticated_user(self, user: User) -> AuthenticatedUser:
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


class JWTTokenService:
    """Servicio para manejo de tokens JWT"""
    
    def __init__(self):
        self.secret_key = getattr(settings, 'SECRET_KEY', 'your-secret-key')
        self.algorithm = 'HS256'
        self.access_token_lifetime = timedelta(hours=1)
        self.refresh_token_lifetime = timedelta(days=7)
    
    def generate_access_token(self, user: AuthenticatedUser) -> str:
        """Genera un access token JWT"""
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'permissions': user.permissions,
            'token_type': 'access',
            'exp': datetime.utcnow() + self.access_token_lifetime,
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def generate_refresh_token(self, user: AuthenticatedUser) -> str:
        """Genera un refresh token JWT"""
        payload = {
            'user_id': user.id,
            'token_type': 'refresh',
            'exp': datetime.utcnow() + self.refresh_token_lifetime,
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def generate_tokens(self, user: AuthenticatedUser) -> AuthToken:
        """Genera ambos tokens (access y refresh)"""
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=int(self.access_token_lifetime.total_seconds())
        )
    
    def validate_access_token(self, token: str) -> Optional[dict]:
        """Valida un access token y retorna el payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get('token_type') != 'access':
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def validate_refresh_token(self, token: str) -> Optional[dict]:
        """Valida un refresh token y retorna el payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            if payload.get('token_type') != 'refresh':
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
