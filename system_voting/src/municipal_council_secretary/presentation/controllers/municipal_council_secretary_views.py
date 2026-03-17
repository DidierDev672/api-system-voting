"""
Municipal Council Secretary Controllers
Presentation Layer - API Views
Vertical Slicing + Hexagonal Architecture
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from system_voting.src.municipal_council_secretary.domain.entities.municipal_council_secretary import (
    CreateMunicipalCouncilSecretaryDTO,
)
from system_voting.src.municipal_council_secretary.infrastructure.adapters.supabase_municipal_council_secretary_repository import (
    SupabaseMunicipalCouncilSecretaryRepository,
)
from system_voting.src.municipal_council_secretary.application.use_cases.municipal_council_secretary_use_cases import (
    CreateMunicipalCouncilSecretaryUseCase,
    GetAllMunicipalCouncilSecretariesUseCase,
    GetMunicipalCouncilSecretaryByIdUseCase,
    UpdateMunicipalCouncilSecretaryUseCase,
    DeleteMunicipalCouncilSecretaryUseCase,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class MunicipalCouncilSecretaryListCreateView(APIView):
    """View for listing and creating municipal council secretaries"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseMunicipalCouncilSecretaryRepository()

    def get(self, request):
        """GET /api/v1/municipal-council-secretaries/ - Get all secretaries"""
        logger.info("=== VIEW: GET /api/v1/municipal-council-secretaries/ ===")

        try:
            use_case = GetAllMunicipalCouncilSecretariesUseCase(self.repository)
            secretaries = use_case.execute()

            data = []
            for s in secretaries:
                data.append(
                    {
                        "id": s.id,
                        "full_name": s.full_name,
                        "document_type": s.document_type,
                        "document_id": s.document_id,
                        "exact_position": s.exact_position,
                        "administrative_act": s.administrative_act,
                        "possession_date": s.possession_date,
                        "legal_period": s.legal_period,
                        "professional_title": s.professional_title,
                        "performance_type": s.performance_type,
                        "institutional_email": s.institutional_email,
                        "digital_signature": s.digital_signature,
                        "created_at": str(s.created_at) if s.created_at else None,
                        "updated_at": str(s.updated_at) if s.updated_at else None,
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
        """POST /api/v1/municipal-council-secretaries/ - Create a new secretary"""
        logger.info("=== VIEW: POST /api/v1/municipal-council-secretaries/ ===")

        try:
            data = request.data

            secretary_dto = CreateMunicipalCouncilSecretaryDTO(
                full_name=data.get("full_name", ""),
                document_type=data.get("document_type", ""),
                document_id=data.get("document_id", ""),
                exact_position=data.get("exact_position", ""),
                administrative_act=data.get("administrative_act", ""),
                possession_date=data.get("possession_date", ""),
                legal_period=data.get("legal_period", ""),
                professional_title=data.get("professional_title"),
                performance_type=data.get("performance_type", ""),
                institutional_email=data.get("institutional_email", ""),
                digital_signature=data.get("digital_signature"),
            )

            use_case = CreateMunicipalCouncilSecretaryUseCase(self.repository)
            result = use_case.execute(secretary_dto)

            return Response(
                {
                    "success": True,
                    "message": "Secretario de consejo municipal creado exitosamente",
                    "data": {
                        "id": result.id,
                        "full_name": result.full_name,
                        "document_type": result.document_type,
                        "document_id": result.document_id,
                        "exact_position": result.exact_position,
                        "administrative_act": result.administrative_act,
                        "possession_date": result.possession_date,
                        "legal_period": result.legal_period,
                        "professional_title": result.professional_title,
                        "performance_type": result.performance_type,
                        "institutional_email": result.institutional_email,
                        "digital_signature": result.digital_signature,
                        "created_at": str(result.created_at)
                        if result.created_at
                        else None,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW VALIDATION ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class MunicipalCouncilSecretaryDetailView(APIView):
    """View for getting, updating, deleting a specific secretary"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseMunicipalCouncilSecretaryRepository()

    def _format_secretary(self, secretary):
        """Format secretary entity to dict"""
        return {
            "id": secretary.id,
            "full_name": secretary.full_name,
            "document_type": secretary.document_type,
            "document_id": secretary.document_id,
            "exact_position": secretary.exact_position,
            "administrative_act": secretary.administrative_act,
            "possession_date": secretary.possession_date,
            "legal_period": secretary.legal_period,
            "professional_title": secretary.professional_title,
            "performance_type": secretary.performance_type,
            "institutional_email": secretary.institutional_email,
            "digital_signature": secretary.digital_signature,
            "created_at": str(secretary.created_at) if secretary.created_at else None,
            "updated_at": str(secretary.updated_at) if secretary.updated_at else None,
        }

    def get(self, request, secretary_id):
        """GET /api/v1/municipal-council-secretaries/{id}/ - Get a specific secretary"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-secretaries/{secretary_id}/ ==="
        )

        try:
            use_case = GetMunicipalCouncilSecretaryByIdUseCase(self.repository)
            secretary = use_case.execute(secretary_id)

            return Response(
                {"success": True, "data": self._format_secretary(secretary)},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request, secretary_id):
        """PUT /api/v1/municipal-council-secretaries/{id}/ - Update a secretary"""
        logger.info(
            f"=== VIEW: PUT /api/v1/municipal-council-secretaries/{secretary_id}/ ==="
        )

        try:
            data = request.data

            use_case = UpdateMunicipalCouncilSecretaryUseCase(self.repository)
            secretary = use_case.execute(secretary_id, data)

            return Response(
                {
                    "success": True,
                    "message": "Secretario de consejo municipal actualizado exitosamente",
                    "data": self._format_secretary(secretary),
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW VALIDATION ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, secretary_id):
        """DELETE /api/v1/municipal-council-secretaries/{id}/ - Delete a secretary"""
        logger.info(
            f"=== VIEW: DELETE /api/v1/municipal-council-secretaries/{secretary_id}/ ==="
        )

        try:
            use_case = DeleteMunicipalCouncilSecretaryUseCase(self.repository)
            use_case.execute(secretary_id)

            return Response(
                {
                    "success": True,
                    "message": "Secretario de consejo municipal eliminado exitosamente",
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            logger.warning(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
