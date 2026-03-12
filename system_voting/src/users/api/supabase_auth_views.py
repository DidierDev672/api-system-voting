from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..application.services.supabase_auth_service import (
    SupabaseAuthService, 
    RegisterRequest, 
    LoginRequest, 
    AuthResponse
)


class SupabaseLoginView(APIView):
    """Vista para login con Supabase Auth"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        self.auth_service = SupabaseAuthService()
    
    def post(self, request):
        """Endpoint POST /api/users/login/"""
        try:
            data = request.data
            
            # Validaciones básicas
            if not data.get("email"):
                return Response({
                    "success": False,
                    "error": "El correo electrónico es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get("password"):
                return Response({
                    "success": False,
                    "error": "La contraseña es obligatoria"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear solicitud de login
            login_request = LoginRequest(
                email=data["email"],
                password=data["password"]
            )
            
            # Ejecutar login
            auth_response = self.auth_service.login(login_request)
            
            if auth_response.success:
                return Response({
                    "success": True,
                    "message": "Login exitoso",
                    "data": {
                        "user": auth_response.user,
                        "session": auth_response.session
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": auth_response.error
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error interno del servidor: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupabaseRegisterView(APIView):
    """Vista para registro con Supabase Auth"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        self.auth_service = SupabaseAuthService()
    
    def post(self, request):
        """Endpoint POST /api/users/register/"""
        try:
            data = request.data
            
            # Validaciones básicas
            required_fields = ["email", "password", "full_name"]
            for field in required_fields:
                if not data.get(field):
                    return Response({
                        "success": False,
                        "error": f"El campo {field} es obligatorio"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar formato de email
            # email = data["email"].strip()
            # if "@" not in email:
            #     return Response({
            #         "success": False,
            #         "error": "El correo electrónico no es válido"
            #     }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validar longitud de contraseña
            password = data["password"]
            if len(password) < 6:
                return Response({
                    "success": False,
                    "error": "La contraseña debe tener al menos 6 caracteres"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear solicitud de registro
            register_request = RegisterRequest(
                email=email,
                password=password,
                full_name=data["full_name"].strip(),
                phone=data.get("phone", "").strip() if data.get("phone") else None
            )
            
            # Ejecutar registro
            auth_response = self.auth_service.register(register_request)
            
            if auth_response.success:
                return Response({
                    "success": True,
                    "message": "Usuario registrado exitosamente",
                    "data": {
                        "user": auth_response.user,
                        "session": auth_response.session
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "success": False,
                    "error": auth_response.error
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error interno del servidor: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupabaseLogoutView(APIView):
    """Vista para logout con Supabase Auth"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        self.auth_service = SupabaseAuthService()
    
    def post(self, request):
        """Endpoint POST /api/users/logout/"""
        try:
            # Obtener token del header
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return Response({
                    "success": False,
                    "error": "Token de autenticación no proporcionado"
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token = auth_header.split(' ')[1]
            
            # Ejecutar logout
            auth_response = self.auth_service.logout(access_token)
            
            if auth_response.success:
                return Response({
                    "success": True,
                    "message": "Sesión cerrada exitosamente"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": auth_response.error
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error interno del servidor: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupabaseProfileView(APIView):
    """Vista para obtener perfil de usuario con Supabase Auth"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        self.auth_service = SupabaseAuthService()
    
    def get(self, request):
        """Endpoint GET /api/users/profile/"""
        try:
            # Obtener token del header
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return Response({
                    "success": False,
                    "error": "Token de autenticación no proporcionado"
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            access_token = auth_header.split(' ')[1]
            
            # Obtener usuario actual
            auth_response = self.auth_service.get_current_user(access_token)
            
            if auth_response.success:
                return Response({
                    "success": True,
                    "message": "Perfil obtenido exitosamente",
                    "data": {
                        "user": auth_response.user
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": auth_response.error
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error interno del servidor: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupabaseRefreshTokenView(APIView):
    """Vista para refrescar token con Supabase Auth"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        self.auth_service = SupabaseAuthService()
    
    def post(self, request):
        """Endpoint POST /api/users/refresh/"""
        try:
            data = request.data
            
            if not data.get("refresh_token"):
                return Response({
                    "success": False,
                    "error": "El refresh token es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Refrescar token
            auth_response = self.auth_service.refresh_token(data["refresh_token"])
            
            if auth_response.success:
                return Response({
                    "success": True,
                    "message": "Token refrescado exitosamente",
                    "data": {
                        "session": auth_response.session
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": auth_response.error
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error interno del servidor: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
