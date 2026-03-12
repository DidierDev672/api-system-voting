"""
Vistas para autenticación y gestión de perfil de usuario
"""

import json
import logging
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from system_voting.src.users.application.services.supabase_auth_service import (
    SupabaseAuthService,
    RegisterRequest,
    LoginRequest,
    AuthResponse,
)
from system_voting.src.users.infrastructure.repositories.supabase_user_repository import (
    SupabaseUserRepository,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class SupabaseRegisterView(View):
    """Vista para registrar usuario en Supabase Auth"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = SupabaseAuthService()
        self.user_repository = SupabaseUserRepository()

    def post(self, request):
        """Registrar usuario en Supabase Auth"""
        logger.info("=== VIEW: POST /auth/register/ - Registro en Supabase Auth ===")

        try:
            body = json.loads(request.body)

            email = body.get("email", "")
            password = body.get("password", "")
            full_name = body.get("full_name", "")
            phone = body.get("phone", "")

            if not email or not password:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "El correo electrónico y la contraseña son requeridos",
                    },
                    status=400,
                )

            register_request = RegisterRequest(
                email=email, password=password, full_name=full_name, phone=phone
            )

            auth_response = self.auth_service.register(register_request)

            if auth_response.success:
                logger.info(
                    f"=== VIEW: Usuario registrado en Auth: {auth_response.user} ==="
                )

                # Crear registro básico en la tabla users con auth_id
                try:
                    user_data = {
                        "auth_id": auth_response.user.get("id"),
                        "email": email,
                        "full_name": full_name,
                        "phone": phone,
                        "document_type": "",
                        "document_number": "",
                        "role": "CITIZEN",
                        "is_active": True,
                    }

                    # Intentar crear el registro de usuario
                    from system_voting.src.users.domain.entities.user import User

                    user = User(**user_data)
                    saved_user = self.user_repository.save(user)

                    logger.info(
                        f"=== VIEW: Registro de usuario creado: {saved_user.id} ==="
                    )

                except Exception as user_error:
                    logger.warning(
                        f"=== VIEW: Error al crear registro de usuario: {str(user_error)} ==="
                    )
                    # El usuario de Auth se creó, el registro en la tabla users puede completarse después

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Usuario registrado exitosamente. Complete su perfil para terminar.",
                        "user": auth_response.user,
                        "session": auth_response.session,
                        "requires_profile_completion": True,
                    },
                    status=201,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": auth_response.error or "Error al registrar usuario",
                    },
                    status=400,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Cuerpo de solicitud inválido"}, status=400
            )
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class SupabaseLoginView(View):
    """Vista para iniciar sesión con Supabase Auth"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = SupabaseAuthService()

    def post(self, request):
        """Iniciar sesión"""
        logger.info("=== VIEW: POST /auth/login/ ===")

        try:
            body = json.loads(request.body)

            login_request = LoginRequest(
                email=body.get("email", ""), password=body.get("password", "")
            )

            auth_response = self.auth_service.login(login_request)

            if auth_response.success:
                logger.info(
                    f"=== VIEW: Login exitoso para: {auth_response.user.get('email')} ==="
                )

                # Obtener datos completos del usuario
                user_repository = SupabaseUserRepository()
                full_user = None

                if auth_response.user:
                    auth_id = auth_response.user.get("id")
                    if auth_id:
                        full_user = user_repository.get_by_auth_id(auth_id)

                user_data = auth_response.user or {}
                if full_user:
                    user_data["full_name"] = full_user.full_name
                    user_data["document_type"] = full_user.document_type
                    user_data["document_number"] = full_user.document_number
                    user_data["phone"] = full_user.phone
                    user_data["role"] = full_user.role

                return JsonResponse(
                    {
                        "success": True,
                        "user": user_data,
                        "session": auth_response.session,
                    },
                    status=200,
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": auth_response.error or "Credenciales inválidas",
                    },
                    status=401,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Cuerpo de solicitud inválido"}, status=400
            )
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"success": False, "error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class CompleteUserProfileView(View):
    """Vista para completar perfil de usuario después del registro en Supabase Auth"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_repository = SupabaseUserRepository()

    def post(self, request):
        """Completar perfil de usuario"""
        logger.info("=== VIEW: POST /auth/complete-profile/ ===")

        try:
            body = json.loads(request.body)

            auth_id = body.get("auth_id", "")
            full_name = body.get("full_name", "")
            document_type = body.get("document_type", "")
            document_number = body.get("document_number", "")
            phone = body.get("phone", "")

            # Validaciones
            if not auth_id:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "El ID de autenticación (auth_id) es requerido",
                    },
                    status=400,
                )

            if not full_name or len(full_name.strip()) < 3:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "El nombre completo debe tener al menos 3 caracteres",
                    },
                    status=400,
                )

            if not document_type:
                return JsonResponse(
                    {"success": False, "error": "El tipo de documento es requerido"},
                    status=400,
                )

            if not document_number or len(document_number.strip()) < 5:
                return JsonResponse(
                    {
                        "success": False,
                        "error": "El número de documento debe tener al menos 5 caracteres",
                    },
                    status=400,
                )

            # Verificar si el usuario ya existe
            existing_user = self.user_repository.get_by_auth_id(auth_id)

            if existing_user:
                # Actualizar usuario existente
                logger.info(
                    f"=== VIEW: Actualizando perfil para auth_id: {auth_id} ==="
                )

                updated_user = self.user_repository.update_by_auth_id(
                    auth_id,
                    {
                        "full_name": full_name,
                        "document_type": document_type,
                        "document_number": document_number,
                        "phone": phone,
                    },
                )

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Perfil actualizado exitosamente",
                        "user": {
                            "id": updated_user.id,
                            "auth_id": updated_user.auth_id,
                            "full_name": updated_user.full_name,
                            "document_type": updated_user.document_type,
                            "document_number": updated_user.document_number,
                            "email": updated_user.email,
                            "phone": updated_user.phone,
                            "role": updated_user.role,
                        },
                    },
                    status=200,
                )
            else:
                # Crear nuevo registro de usuario
                logger.info(f"=== VIEW: Creando perfil para auth_id: {auth_id} ===")

                from system_voting.src.users.domain.entities.user import User

                user = User(
                    auth_id=auth_id,
                    full_name=full_name,
                    document_type=document_type,
                    document_number=document_number,
                    phone=phone,
                    email="",  # Se obtendrá del token
                    role="CITIZEN",
                    is_active=True,
                )

                saved_user = self.user_repository.save(user)

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Perfil creado exitosamente",
                        "user": {
                            "id": saved_user.id,
                            "auth_id": saved_user.auth_id,
                            "full_name": saved_user.full_name,
                            "document_type": saved_user.document_type,
                            "document_number": saved_user.document_number,
                            "email": saved_user.email,
                            "phone": saved_user.phone,
                            "role": saved_user.role,
                        },
                    },
                    status=201,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Cuerpo de solicitud inválido"}, status=400
            )
        except ValueError as ve:
            return JsonResponse({"success": False, "error": str(ve)}, status=400)
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def get(self, request):
        """Obtener perfil del usuario actual"""
        logger.info("=== VIEW: GET /auth/complete-profile/ ===")

        # Obtener token del header
        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"success": False, "error": "Token de autorización requerido"},
                status=401,
            )

        access_token = auth_header.split(" ")[1]

        # Verificar token con Supabase
        auth_service = SupabaseAuthService()
        auth_response = auth_service.get_current_user(access_token)

        if not auth_response.success:
            return JsonResponse(
                {"success": False, "error": auth_response.error or "Token inválido"},
                status=401,
            )

        # Obtener datos del usuario de la tabla users
        auth_id = auth_response.user.get("id")
        user = self.user_repository.get_by_auth_id(auth_id)

        if not user:
            return JsonResponse(
                {"success": False, "error": "Perfil de usuario no encontrado"},
                status=404,
            )

        return JsonResponse(
            {
                "success": True,
                "user": {
                    "id": user.id,
                    "auth_id": user.auth_id,
                    "full_name": user.full_name,
                    "document_type": user.document_type,
                    "document_number": user.document_number,
                    "email": user.email,
                    "phone": user.phone,
                    "role": user.role,
                    "is_active": user.is_active,
                },
            },
            status=200,
        )


@method_decorator(csrf_exempt, name="dispatch")
class SupabaseLogoutView(View):
    """Vista para cerrar sesión"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = SupabaseAuthService()

    def post(self, request):
        """Cerrar sesión"""
        logger.info("=== VIEW: POST /auth/logout/ ===")

        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"success": False, "error": "Token de autorización requerido"},
                status=401,
            )

        access_token = auth_header.split(" ")[1]

        auth_response = self.auth_service.logout(access_token)

        if auth_response.success:
            return JsonResponse(
                {"success": True, "message": "Sesión cerrada exitosamente"}, status=200
            )
        else:
            return JsonResponse(
                {"success": False, "error": auth_response.error}, status=400
            )


@method_decorator(csrf_exempt, name="dispatch")
class SupabaseProfileView(View):
    """Vista para obtener perfil del usuario"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = SupabaseAuthService()
        self.user_repository = SupabaseUserRepository()

    def get(self, request):
        """Obtener perfil"""
        logger.info("=== VIEW: GET /auth/profile/ ===")

        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"success": False, "error": "Token de autorización requerido"},
                status=401,
            )

        access_token = auth_header.split(" ")[1]

        auth_response = self.auth_service.get_current_user(access_token)

        if not auth_response.success:
            return JsonResponse(
                {"success": False, "error": auth_response.error}, status=401
            )

        # Obtener datos completos del usuario
        auth_id = auth_response.user.get("id")
        user = self.user_repository.get_by_auth_id(auth_id)

        if user:
            return JsonResponse(
                {
                    "success": True,
                    "user": {
                        "id": user.id,
                        "auth_id": user.auth_id,
                        "full_name": user.full_name,
                        "document_type": user.document_type,
                        "document_number": user.document_number,
                        "email": user.email,
                        "phone": user.phone,
                        "role": user.role,
                        "is_active": user.is_active,
                    },
                },
                status=200,
            )
        else:
            # Devolver datos básicos del auth
            return JsonResponse(
                {"success": True, "user": auth_response.user}, status=200
            )


@method_decorator(csrf_exempt, name="dispatch")
class SupabaseRefreshTokenView(View):
    """Vista para refrescar token"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = SupabaseAuthService()

    def post(self, request):
        """Refrescar token"""
        logger.info("=== VIEW: POST /auth/refresh/ ===")

        try:
            body = json.loads(request.body)
            refresh_token = body.get("refresh_token", "")

            if not refresh_token:
                return JsonResponse(
                    {"success": False, "error": "Refresh token es requerido"},
                    status=400,
                )

            auth_response = self.auth_service.refresh_token(refresh_token)

            if auth_response.success:
                return JsonResponse(
                    {"success": True, "session": auth_response.session}, status=200
                )
            else:
                return JsonResponse(
                    {"success": False, "error": auth_response.error}, status=401
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Cuerpo de solicitud inválido"}, status=400
            )
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
