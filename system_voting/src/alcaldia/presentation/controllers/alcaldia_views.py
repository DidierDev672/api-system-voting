"""
Views - Alcaldia
Presentation Layer
SOLID Principles - Controller Pattern
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from system_voting.src.alcaldia.application.use_cases.alcaldia_use_cases import (
    CreateAlcaldiaUseCase,
    GetAllAlcaldiasUseCase,
    GetAlcaldiaByIdUseCase,
    UpdateAlcaldiaUseCase,
    DeleteAlcaldiaUseCase,
)
from system_voting.src.alcaldia.infrastructure.adapters.supabase_alcaldia_repository import (
    SupabaseAlcaldiaRepository,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class AlcaldiaListCreateView(APIView):
    """View for listing and creating alcaldias"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseAlcaldiaRepository()

    def get(self, request):
        """GET /api/v1/alcaldias/ - Get all alcaldias"""
        logger.info("=== VIEW: GET /api/v1/alcaldias/ ===")

        try:
            use_case = GetAllAlcaldiasUseCase(self.repository)
            alcaldias = use_case.execute()

            data = []
            for a in alcaldias:
                data.append(
                    {
                        "id": a.id,
                        "nombre_entidad": a.nombre_entidad,
                        "nit": a.nit,
                        "codigo_sigep": a.codigo_sigep,
                        "orden_entidad": a.orden_entidad,
                        "municipio": a.municipio,
                        "direccion_fisica": a.direccion_fisica,
                        "dominio": a.dominio,
                        "correo_institucional": a.correo_institucional,
                        "id_alcalde": a.id_alcalde,
                        "nombre_alcalde": a.nombre_alcalde,
                        "acto_posesion": a.acto_posesion,
                        "created_at": str(a.created_at) if a.created_at else None,
                        "updated_at": str(a.updated_at) if a.updated_at else None,
                    }
                )

            return Response(
                {"success": True, "data": data, "count": len(data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """POST /api/v1/alcaldias/ - Create a new alcaldia"""
        logger.info("=== VIEW: POST /api/v1/alcaldias/ ===")

        try:
            data = request.data

            create_dto = {
                "nombre_entidad": data.get("nombre_entidad"),
                "nit": data.get("nit"),
                "codigo_sigep": data.get("codigo_sigep"),
                "orden_entidad": data.get("orden_entidad"),
                "municipio": data.get("municipio"),
                "direccion_fisica": data.get("direccion_fisica"),
                "dominio": data.get("dominio"),
                "correo_institucional": data.get("correo_institucional"),
                "id_alcalde": data.get("id_alcalde"),
                "nombre_alcalde": data.get("nombre_alcalde"),
                "acto_posesion": data.get("acto_posesion"),
            }

            from system_voting.src.alcaldia.domain.entities.alcaldia import (
                CreateAlcaldiaDTO,
            )

            dto = CreateAlcaldiaDTO(**create_dto)

            use_case = CreateAlcaldiaUseCase(self.repository)
            alcaldia = use_case.execute(dto)

            response_data = {
                "id": alcaldia.id,
                "nombre_entidad": alcaldia.nombre_entidad,
                "nit": alcaldia.nit,
                "codigo_sigep": alcaldia.codigo_sigep,
                "orden_entidad": alcaldia.orden_entidad,
                "municipio": alcaldia.municipio,
                "direccion_fisica": alcaldia.direccion_fisica,
                "dominio": alcaldia.dominio,
                "correo_institucional": alcaldia.correo_institucional,
                "id_alcalde": alcaldia.id_alcalde,
                "nombre_alcalde": alcaldia.nombre_alcalde,
                "acto_posesion": alcaldia.acto_posesion,
                "created_at": str(alcaldia.created_at) if alcaldia.created_at else None,
                "updated_at": str(alcaldia.updated_at) if alcaldia.updated_at else None,
            }

            return Response(
                {
                    "success": True,
                    "message": "Alcaldía creada exitosamente",
                    "data": response_data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class AlcaldiaDetailView(APIView):
    """View for getting, updating, deleting a specific alcaldia"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseAlcaldiaRepository()

    def _format_alcaldia(self, alcaldia):
        """Format alcaldia entity to dict"""
        return {
            "id": alcaldia.id,
            "nombre_entidad": alcaldia.nombre_entidad,
            "nit": alcaldia.nit,
            "codigo_sigep": alcaldia.codigo_sigep,
            "orden_entidad": alcaldia.orden_entidad,
            "municipio": alcaldia.municipio,
            "direccion_fisica": alcaldia.direccion_fisica,
            "dominio": alcaldia.dominio,
            "correo_institucional": alcaldia.correo_institucional,
            "id_alcalde": alcaldia.id_alcalde,
            "nombre_alcalde": alcaldia.nombre_alcalde,
            "acto_posesion": alcaldia.acto_posesion,
            "created_at": str(alcaldia.created_at) if alcaldia.created_at else None,
            "updated_at": str(alcaldia.updated_at) if alcaldia.updated_at else None,
        }

    def get(self, request, alcaldia_id):
        """GET /api/v1/alcaldias/<id>/ - Get alcaldia by ID"""
        logger.info(f"=== VIEW: GET /api/v1/alcaldias/{alcaldia_id}/ ===")

        try:
            use_case = GetAlcaldiaByIdUseCase(self.repository)
            alcaldia = use_case.execute(alcaldia_id)

            return Response(
                {
                    "success": True,
                    "data": self._format_alcaldia(alcaldia),
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, alcaldia_id):
        """PUT /api/v1/alcaldias/<id>/ - Update alcaldia"""
        logger.info(f"=== VIEW: PUT /api/v1/alcaldias/{alcaldia_id}/ ===")

        try:
            data = request.data

            update_data = {}
            for field in [
                "nombre_entidad",
                "nit",
                "codigo_sigep",
                "orden_entidad",
                "municipio",
                "direccion_fisica",
                "dominio",
                "correo_institucional",
                "id_alcalde",
                "nombre_alcalde",
                "acto_posesion",
            ]:
                if field in data:
                    update_data[field] = data[field]

            from system_voting.src.alcaldia.domain.entities.alcaldia import (
                UpdateAlcaldiaDTO,
            )

            dto = UpdateAlcaldiaDTO(**update_data)

            use_case = UpdateAlcaldiaUseCase(self.repository)
            alcaldia = use_case.execute(alcaldia_id, dto)

            return Response(
                {
                    "success": True,
                    "message": "Alcaldía actualizada exitosamente",
                    "data": self._format_alcaldia(alcaldia),
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, alcaldia_id):
        """DELETE /api/v1/alcaldias/<id>/ - Delete alcaldia"""
        logger.info(f"=== VIEW: DELETE /api/v1/alcaldias/{alcaldia_id}/ ===")

        try:
            use_case = DeleteAlcaldiaUseCase(self.repository)
            use_case.execute(alcaldia_id)

            return Response(
                {
                    "success": True,
                    "message": "Alcaldía eliminada exitosamente",
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
