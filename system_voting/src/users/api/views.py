from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from system_voting.src.users.application.services.user_service import UserService
from system_voting.src.users.infrastructure.repositories.supabase_user_repository import SupabaseUserRepository
from system_voting.src.users.domain.entities.user import CreateUserCommand, UpdateUserCommand


class RegisterUserView(APIView):
    """Vista API - Vertical Slicing: Registro de Usuarios"""
    
    def __init__(self):
        super().__init__()
        # Inyección de dependencias - Hexagonal
        user_repository = SupabaseUserRepository()
        self.user_service = UserService(user_repository)
    
    def post(self, request):
        """Endpoint POST /api/users/register/"""
        try:
            # Validar tipos de documento permitidos
            valid_document_types = [
                'CC',  # Cédula de Ciudadanía
                'CE',  # Cédula de Extranjería
                'PA',  # Pasaporte
                'TI',  # Tarjeta de Identidad
                'RC'   # Registro Civil
            ]
            
            data = request.data
            
            # Validaciones básicas
            if not data.get("full_name"):
                return Response({
                    "error": "Error de validación",
                    "message": "El nombre completo es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("document_type"):
                return Response({
                    "error": "Error de validación", 
                    "message": "El tipo de documento es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if data.get("document_type") not in valid_document_types:
                return Response({
                    "error": "Error de validación",
                    "message": f"Tipo de documento no válido. Opciones: {', '.join(valid_document_types)}"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("document_number"):
                return Response({
                    "error": "Error de validación",
                    "message": "El número de documento es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("email"):
                return Response({
                    "error": "Error de validación",
                    "message": "El correo electrónico es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear comando de aplicación
            command = CreateUserCommand(
                full_name=data["full_name"],
                document_type=data["document_type"],
                document_number=data["document_number"],
                email=data["email"],
                password=data.get("password"),
                phone=data.get("phone"),
                role=data.get("role", "CITIZEN")
            )
            
            # Ejecutar caso de uso
            user = self.user_service.create_user(command)
            
            return Response({
                "message": "Usuario registrado exitosamente",
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "document_type": user.document_type,
                    "document_number": user.document_number,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "is_active": user.is_active
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
                "message": "Ocurrió un error inesperado al registrar el usuario"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUsersView(APIView):
    """Vista API - Vertical Slicing: Listado de Usuarios"""
    
    def __init__(self):
        super().__init__()
        user_repository = SupabaseUserRepository()
        self.user_service = UserService(user_repository)
    
    def get(self, request):
        """Endpoint GET /api/users/"""
        try:
            # Obtener parámetros de consulta
            active_only = request.GET.get('active_only', 'true').lower() == 'true'
            
            # Ejecutar caso de uso
            users = self.user_service.get_users(active_only)
            
            # Formatear respuesta
            users_data = []
            for user in users:
                users_data.append({
                    "id": user.id,
                    "full_name": user.full_name,
                    "document_type": user.document_type,
                    "document_number": user.document_number,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "is_active": user.is_active
                })
            
            return Response({
                "message": "Usuarios obtenidos exitosamente",
                "data": users_data,
                "total": len(users_data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al obtener los usuarios"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserView(APIView):
    """Vista API - Vertical Slicing: Obtener Usuario por ID"""
    
    def __init__(self):
        super().__init__()
        user_repository = SupabaseUserRepository()
        self.user_service = UserService(user_repository)
    
    def get(self, request, user_id):
        """Endpoint GET /api/users/{user_id}/"""
        try:
            user = self.user_service.get_user_by_id(user_id)
            
            if not user:
                return Response({
                    "error": "Usuario no encontrado",
                    "message": "No se encontró un usuario con el ID proporcionado"
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "message": "Usuario obtenido exitosamente",
                "data": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "document_type": user.document_type,
                    "document_number": user.document_number,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "is_active": user.is_active
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error interno del servidor",
                "message": "Error al obtener el usuario"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)