from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

from ..application.services.auth_service import AuthService
from ..infrastructure.repositories.supabase_auth_repository import SupabaseAuthRepository
from ..infrastructure.repositories.supabase_user_repository import SupabaseUserRepository
from ..infrastructure.repositories.supabase_permission_repository import SupabasePermissionRepository


class JWTAuthentication(BaseAuthentication):
    """Middleware de Autenticación JWT - Vertical Slicing + Hexagonal"""
    
    def __init__(self):
        super().__init__()
        # Inicializar servicios una sola vez
        user_repository = SupabaseUserRepository()
        permission_repository = SupabasePermissionRepository()
        auth_repository = SupabaseAuthRepository(user_repository, permission_repository)
        self.auth_service = AuthService(auth_repository, user_repository, permission_repository)
    
    def authenticate(self, request):
        """Autentica la request usando token JWT"""
        # Obtener token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None  # No hay token, no autenticar
        
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Formato de token inválido. Use: Bearer <token>')
        
        token = auth_header[7:]  # Remover 'Bearer '
        
        # Validar token y obtener usuario
        try:
            user = self.auth_service.get_current_user(token)
            if not user:
                raise AuthenticationFailed('Token inválido o expirado')
            
            # Añadir información del usuario a la request
            request.user = user
            request.user_id = user.id
            request.user_permissions = user.permissions
            request.user_role = user.role
            
            return (user, token)
            
        except AuthenticationFailed:
            raise
        except Exception as e:
            raise AuthenticationFailed('Error de autenticación')
    
    def authenticate_header(self, request):
        """Retorna el header de autenticación esperado"""
        return 'Bearer'


def require_permission(permission):
    """Decorador para requerir permisos específicos"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not hasattr(request, 'user') or not request.user:
                return JsonResponse({
                    "error": "No autorizado",
                    "message": "Se requiere autenticación"
                }, status=401)
            
            # Verificar permiso específico
            if not request.user.has_permission(permission):
                return JsonResponse({
                    "error": "Prohibido",
                    "message": f"Se requiere el permiso: {permission}"
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_role(role):
    """Decorador para requerir roles específicos"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not hasattr(request, 'user') or not request.user:
                return JsonResponse({
                    "error": "No autorizado",
                    "message": "Se requiere autenticación"
                }, status=401)
            
            # Verificar rol específico
            if request.user.role != role:
                return JsonResponse({
                    "error": "Prohibido",
                    "message": f"Se requiere el rol: {role}"
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_any_permission(permissions):
    """Decorador para requerir al menos uno de los permisos"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not hasattr(request, 'user') or not request.user:
                return JsonResponse({
                    "error": "No autorizado",
                    "message": "Se requiere autenticación"
                }, status=401)
            
            # Verificar si tiene al menos uno de los permisos
            if not request.user.has_any_permission(permissions):
                return JsonResponse({
                    "error": "Prohibido",
                    "message": f"Se requiere al menos uno de estos permisos: {', '.join(permissions)}"
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_all_permissions(permissions):
    """Decorador para requerir todos los permisos"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not hasattr(request, 'user') or not request.user:
                return JsonResponse({
                    "error": "No autorizado",
                    "message": "Se requiere autenticación"
                }, status=401)
            
            # Verificar si tiene todos los permisos
            if not request.user.has_all_permissions(permissions):
                return JsonResponse({
                    "error": "Prohibido",
                    "message": f"Se requieren todos estos permisos: {', '.join(permissions)}"
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Decoradores específicos para roles comunes
require_super_admin = require_role('SUPER_ADMIN')
require_representative = require_role('REPRESENTATIVE')
require_member = require_role('MEMBER')

# Decoradores específicos para permisos comunes
require_manage_users = require_permission('manage_users')
require_manage_system = require_permission('manage_system')
require_create_voting = require_permission('create_voting')
require_vote = require_permission('vote')
