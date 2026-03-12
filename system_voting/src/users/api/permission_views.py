from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..application.services.permission_service import PermissionService
from ..infrastructure.repositories.supabase_permission_repository import SupabasePermissionRepository
from ..infrastructure.repositories.supabase_user_repository import SupabaseUserRepository
from ..domain.entities.permission import (
    CreatePermissionCommand, 
    UpdatePermissionCommand,
    AssignPermissionCommand,
    RevokePermissionCommand
)


class CreatePermissionView(APIView):
    """Vista API - Vertical Slicing: Crear Permisos de Usuario"""
    
    def __init__(self):
        super().__init__()
        # Inyección de dependencias - Hexagonal
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def post(self, request):
        """Endpoint POST /api/users/permissions/"""
        try:
            data = request.data
            
            # Validaciones básicas
            if not data.get("user_id"):
                return Response({
                    "error": "Error de validación",
                    "message": "El ID del usuario es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("role"):
                return Response({
                    "error": "Error de validación",
                    "message": "El rol es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar roles permitidos
            valid_roles = ["SUPER_ADMIN", "REPRESENTATIVE", "MEMBER", "CITIZEN"]
            if data["role"].upper() not in valid_roles:
                return Response({
                    "error": "Error de validación",
                    "message": f"Rol no válido. Opciones: {', '.join(valid_roles)}"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear comando de aplicación
            command = CreatePermissionCommand(
                user_id=data["user_id"],
                role=data["role"],
                assigned_by=request.user.id if hasattr(request, 'user') else None,
                additional_permissions=data.get("additional_permissions", [])
            )
            
            # Ejecutar caso de uso
            user_permission = self.permission_service.create_user_permissions(command)
            
            return Response({
                "message": "Permisos creados exitosamente",
                "data": {
                    "id": user_permission.id,
                    "user_id": user_permission.user_id,
                    "role": user_permission.role.role_name,
                    "permissions": [perm.value for perm in user_permission.get_all_permissions()],
                    "additional_permissions": [perm.value for perm in user_permission.additional_permissions],
                    "assigned_by": user_permission.assigned_by,
                    "assigned_at": user_permission.assigned_at.isoformat() if user_permission.assigned_at else None,
                    "is_active": user_permission.is_active
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                "error": "Error de validación",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Ocurrió un error inesperado al crear los permisos"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserPermissionView(APIView):
    """Vista API - Vertical Slicing: Obtener Permisos de Usuario"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def get(self, request, user_id):
        """Endpoint GET /api/users/{user_id}/permissions/"""
        try:
            user_permission = self.permission_service.get_user_permissions(user_id)
            
            if not user_permission:
                return Response({
                    "error": "Permisos no encontrados",
                    "message": "El usuario no tiene permisos registrados"
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "message": "Permisos obtenidos exitosamente",
                "data": {
                    "id": user_permission.id,
                    "user_id": user_permission.user_id,
                    "role": user_permission.role.role_name,
                    "permissions": [perm.value for perm in user_permission.get_all_permissions()],
                    "additional_permissions": [perm.value for perm in user_permission.additional_permissions],
                    "assigned_by": user_permission.assigned_by,
                    "assigned_at": user_permission.assigned_at.isoformat() if user_permission.assigned_at else None,
                    "is_active": user_permission.is_active
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al obtener los permisos del usuario"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePermissionView(APIView):
    """Vista API - Vertical Slicing: Actualizar Permisos de Usuario"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def put(self, request, permission_id):
        """Endpoint PUT /api/users/permissions/{permission_id}/"""
        try:
            data = request.data
            
            # Validar rol si se proporciona
            if data.get("role"):
                valid_roles = ["SUPER_ADMIN", "REPRESENTATIVE", "MEMBER", "CITIZEN"]
                if data["role"].upper() not in valid_roles:
                    return Response({
                        "error": "Error de validación",
                        "message": f"Rol no válido. Opciones: {', '.join(valid_roles)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear comando de actualización
            command = UpdatePermissionCommand(
                id=permission_id,
                role=data.get("role"),
                additional_permissions=data.get("additional_permissions"),
                is_active=data.get("is_active")
            )
            
            # Ejecutar caso de uso
            user_permission = self.permission_service.update_user_permissions(command)
            
            return Response({
                "message": "Permisos actualizados exitosamente",
                "data": {
                    "id": user_permission.id,
                    "user_id": user_permission.user_id,
                    "role": user_permission.role.role_name,
                    "permissions": [perm.value for perm in user_permission.get_all_permissions()],
                    "additional_permissions": [perm.value for perm in user_permission.additional_permissions],
                    "is_active": user_permission.is_active
                }
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                "error": "Error de validación",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al actualizar los permisos"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AssignPermissionView(APIView):
    """Vista API - Vertical Slicing: Asignar Permiso Adicional"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def post(self, request):
        """Endpoint POST /api/users/permissions/assign/"""
        try:
            data = request.data
            
            if not data.get("user_id"):
                return Response({
                    "error": "Error de validación",
                    "message": "El ID del usuario es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("permission"):
                return Response({
                    "error": "Error de validación",
                    "message": "El permiso es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear comando
            command = AssignPermissionCommand(
                user_id=data["user_id"],
                permission=data["permission"],
                assigned_by=request.user.id if hasattr(request, 'user') else None
            )
            
            # Ejecutar caso de uso
            user_permission = self.permission_service.assign_additional_permission(command)
            
            return Response({
                "message": "Permiso asignado exitosamente",
                "data": {
                    "user_id": user_permission.user_id,
                    "role": user_permission.role.role_name,
                    "assigned_permission": data["permission"],
                    "total_permissions": [perm.value for perm in user_permission.get_all_permissions()]
                }
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                "error": "Error de validación",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al asignar el permiso"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RevokePermissionView(APIView):
    """Vista API - Vertical Slicing: Revocar Permiso Adicional"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def delete(self, request, user_id, permission):
        """Endpoint DELETE /api/users/{user_id}/permissions/{permission}/"""
        try:
            # Crear comando
            command = RevokePermissionCommand(
                user_id=user_id,
                permission=permission
            )
            
            # Ejecutar caso de uso
            user_permission = self.permission_service.revoke_additional_permission(command)
            
            return Response({
                "message": "Permiso revocado exitosamente",
                "data": {
                    "user_id": user_permission.user_id,
                    "role": user_permission.role.role_name,
                    "revoked_permission": permission,
                    "remaining_permissions": [perm.value for perm in user_permission.get_all_permissions()]
                }
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                "error": "Error de validación",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al revocar el permiso"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListPermissionsView(APIView):
    """Vista API - Vertical Slicing: Listar Todos los Permisos"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def get(self, request):
        """Endpoint GET /api/users/permissions/"""
        try:
            # Obtener parámetros de consulta
            role_filter = request.GET.get('role')
            
            if role_filter:
                permissions = self.permission_service.get_permissions_by_role(role_filter)
            else:
                permissions = self.permission_service.get_all_permissions()
            
            # Formatear respuesta
            permissions_data = []
            for perm in permissions:
                permissions_data.append({
                    "id": perm.id,
                    "user_id": perm.user_id,
                    "role": perm.role.role_name,
                    "permissions": [p.value for p in perm.get_all_permissions()],
                    "additional_permissions": [p.value for p in perm.additional_permissions],
                    "assigned_by": perm.assigned_by,
                    "assigned_at": perm.assigned_at.isoformat() if perm.assigned_at else None,
                    "is_active": perm.is_active
                })
            
            return Response({
                "message": "Permisos obtenidos exitosamente",
                "data": permissions_data,
                "total": len(permissions_data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al obtener los permisos"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RolesAndPermissionsView(APIView):
    """Vista API - Vertical Slicing: Obtener Roles y Permisos Disponibles"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def get(self, request):
        """Endpoint GET /api/users/permissions/info/"""
        try:
            roles = self.permission_service.get_available_roles()
            permissions = self.permission_service.get_available_permissions()
            
            return Response({
                "message": "Información de roles y permisos obtenida exitosamente",
                "data": {
                    "roles": roles,
                    "permissions": permissions
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al obtener la información de roles y permisos"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckPermissionView(APIView):
    """Vista API - Vertical Slicing: Verificar Permisos de Usuario"""
    
    def __init__(self):
        super().__init__()
        permission_repository = SupabasePermissionRepository()
        user_repository = SupabaseUserRepository()
        self.permission_service = PermissionService(permission_repository, user_repository)
    
    def post(self, request):
        """Endpoint POST /api/users/permissions/check/"""
        try:
            data = request.data
            
            if not data.get("user_id"):
                return Response({
                    "error": "Error de validación",
                    "message": "El ID del usuario es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("permission"):
                return Response({
                    "error": "Error de validación",
                    "message": "El permiso a verificar es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar permiso individual
            has_permission = self.permission_service.check_user_permission(
                data["user_id"], 
                data["permission"]
            )
            
            response_data = {
                "user_id": data["user_id"],
                "permission": data["permission"],
                "has_permission": has_permission
            }
            
            # Si se proporcionan múltiples permisos, verificar acceso completo
            if data.get("required_permissions"):
                has_access = self.permission_service.check_user_access(
                    data["user_id"],
                    data["required_permissions"]
                )
                response_data["required_permissions"] = data["required_permissions"]
                response_data["has_access"] = has_access
            
            return Response({
                "message": "Verificación de permisos completada",
                "data": response_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al verificar los permisos"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
