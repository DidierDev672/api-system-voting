from typing import Optional, Dict, Any
from dataclasses import dataclass
import json
import hashlib
from supabase import create_client


@dataclass
class AuthResponse:
    """Respuesta de autenticación"""
    success: bool
    user: Optional[Dict[str, Any]] = None
    session: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class RegisterRequest:
    """Solicitud de registro"""
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None


@dataclass
class LoginRequest:
    """Solicitud de login"""
    email: str
    password: str


class SupabaseAuthService:
    """Servicio de autenticación con Supabase Auth"""
    
    def __init__(self):
        # Obtener configuración de Supabase desde settings
        from django.conf import settings
        self.supabase_url = getattr(settings, 'SUPABASE_URL', 'https://your-project.supabase.co')
        self.supabase_key = getattr(settings, 'SUPABASE_ANON_KEY', 'your-anon-key')
        
        # Modo demo para pruebas sin Supabase
        self.demo_mode = self.supabase_url == 'https://your-project.supabase.co'
        
        if not self.demo_mode:
            # Inicializar cliente de Supabase solo si no es modo demo
            self.supabase = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            print("MODO DEMO: Usando autenticación simulada para pruebas")
    
    def register(self, request: RegisterRequest) -> AuthResponse:
        """Registrar un nuevo usuario en Supabase Auth"""
        try:
            if self.demo_mode:
                # Modo demo: simulación de registro
                import uuid
                import datetime
                
                user_id = str(uuid.uuid4())
                return AuthResponse(
                    success=True,
                    user={
                        'id': user_id,
                        'email': request.email,
                        'full_name': request.full_name,
                        'phone': request.phone
                    },
                    session={
                        'access_token': f'demo-access-token-{user_id}',
                        'refresh_token': f'demo-refresh-token-{user_id}',
                        'expires_at': int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
                    }
                )
            
            # Registrar usuario en Supabase Auth
            auth_response = self.supabase.auth.sign_up({
                'email': request.email,
                'password': request.password,
                'options': {
                    'data': {
                        'full_name': request.full_name,
                        'phone': request.phone
                    }
                }
            })
            
            if auth_response.user:
                return AuthResponse(
                    success=True,
                    user={
                        'id': auth_response.user.id,
                        'email': auth_response.user.email,
                        'full_name': auth_response.user.user_metadata.get('full_name', request.full_name),
                        'phone': auth_response.user.user_metadata.get('phone', request.phone)
                    },
                    session={
                        'access_token': auth_response.session.access_token,
                        'refresh_token': auth_response.session.refresh_token,
                        'expires_at': auth_response.session.expires_at
                    }
                )
            else:
                return AuthResponse(
                    success=False,
                    error="No se pudo crear el usuario"
                )
                
        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                error_msg = "El correo electrónico ya está registrado"
            elif "weak password" in error_msg.lower():
                error_msg = "La contraseña es demasiado débil"
            # elif "invalid email" in error_msg.lower():
            #     error_msg = "El correo electrónico no es válido"
            
            return AuthResponse(
                success=False,
                error=error_msg
            )
    
    def login(self, request: LoginRequest) -> AuthResponse:
        """Iniciar sesión con Supabase Auth"""
        try:
            if self.demo_mode:
                # Modo demo: simulación de login
                import uuid
                import datetime
                
                # Simular usuario encontrado
                user_id = str(uuid.uuid4())
                return AuthResponse(
                    success=True,
                    user={
                        'id': user_id,
                        'email': request.email,
                        'full_name': 'Demo User',
                        'phone': None
                    },
                    session={
                        'access_token': f'demo-access-token-{user_id}',
                        'refresh_token': f'demo-refresh-token-{user_id}',
                        'expires_at': int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
                    }
                )
            
            # Iniciar sesión en Supabase Auth
            auth_response = self.supabase.auth.sign_in_with_password({
                'email': request.email,
                'password': request.password
            })
            
            if auth_response.user:
                return AuthResponse(
                    success=True,
                    user={
                        'id': auth_response.user.id,
                        'email': auth_response.user.email,
                        'full_name': auth_response.user.user_metadata.get('full_name', ''),
                        'phone': auth_response.user.user_metadata.get('phone', '')
                    },
                    session={
                        'access_token': auth_response.session.access_token,
                        'refresh_token': auth_response.session.refresh_token,
                        'expires_at': auth_response.session.expires_at
                    }
                )
            else:
                return AuthResponse(
                    success=False,
                    error="Credenciales inválidas"
                )
                
        except Exception as e:
            error_msg = str(e)
            if "invalid login credentials" in error_msg.lower():
                error_msg = "Correo electrónico o contraseña incorrectos"
            elif "email not confirmed" in error_msg.lower():
                error_msg = "El correo electrónico no ha sido confirmado"
            
            return AuthResponse(
                success=False,
                error=error_msg
            )
    
    def logout(self, access_token: str) -> AuthResponse:
        """Cerrar sesión"""
        try:
            self.supabase.auth.sign_out()
            return AuthResponse(success=True)
        except Exception as e:
            return AuthResponse(
                success=False,
                error=f"Error al cerrar sesión: {str(e)}"
            )
    
    def get_current_user(self, access_token: str) -> AuthResponse:
        """Obtener usuario actual a partir del token"""
        try:
            if self.demo_mode:
                # Modo demo: verificar token simulado
                if access_token.startswith('demo-access-token-'):
                    user_id = access_token.replace('demo-access-token-', '')
                    return AuthResponse(
                        success=True,
                        user={
                            'id': user_id,
                            'email': 'demo@example.com',
                            'full_name': 'Demo User',
                            'phone': None
                        }
                    )
                else:
                    return AuthResponse(
                        success=False,
                        error="Token inválido o expirado"
                    )
            
            # Verificar el token y obtener el usuario
            user_response = self.supabase.auth.get_user(access_token)
            
            if user_response.user:
                return AuthResponse(
                    success=True,
                    user={
                        'id': user_response.user.id,
                        'email': user_response.user.email,
                        'full_name': user_response.user.user_metadata.get('full_name', ''),
                        'phone': user_response.user.user_metadata.get('phone', '')
                    }
                )
            else:
                return AuthResponse(
                    success=False,
                    error="Token inválido o expirado"
                )
                
        except Exception as e:
            return AuthResponse(
                success=False,
                error=f"Error al verificar token: {str(e)}"
            )
    
    def refresh_token(self, refresh_token: str) -> AuthResponse:
        """Refrescar el token de acceso"""
        try:
            # Refrescar el token
            session_response = self.supabase.auth.refresh_session(refresh_token)
            
            if session_response.session:
                return AuthResponse(
                    success=True,
                    session={
                        'access_token': session_response.session.access_token,
                        'refresh_token': session_response.session.refresh_token,
                        'expires_at': session_response.session.expires_at
                    }
                )
            else:
                return AuthResponse(
                    success=False,
                    error="No se pudo refrescar el token"
                )
                
        except Exception as e:
            return AuthResponse(
                success=False,
                error=f"Error al refrescar token: {str(e)}"
            )
