"""
Municipal Council President Controllers
Presentation Layer - API Views
Vertical Slicing + Hexagonal Architecture
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from system_voting.src.municipal_council_president.domain.entities.municipal_council_president import (
    CreateMunicipalCouncilPresidentDTO,
)
from system_voting.src.municipal_council_president.infrastructure.adapters.supabase_municipal_council_president_repository import (
    SupabaseMunicipalCouncilPresidentRepository,
)
from system_voting.src.municipal_council_president.application.use_cases.municipal_council_president_use_cases import (
    CreateMunicipalCouncilPresidentUseCase,
    GetAllMunicipalCouncilPresidentsUseCase,
    GetMunicipalCouncilPresidentByIdUseCase,
    UpdateMunicipalCouncilPresidentUseCase,
    DeleteMunicipalCouncilPresidentUseCase,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class MunicipalCouncilPresidentListCreateView(APIView):
    """View for listing and creating municipal council presidents"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseMunicipalCouncilPresidentRepository()

    def get(self, request):
        """GET /api/v1/municipal-council-presidents/ - Get all presidents"""
        logger.info("=== VIEW: GET /api/v1/municipal-council-presidents/ ===")

        try:
            use_case = GetAllMunicipalCouncilPresidentsUseCase(self.repository)
            presidents = use_case.execute()

            data = []
            for p in presidents:
                data.append(
                    {
                        "id": p.id,
                        "full_name": p.full_name,
                        "document_type": p.document_type,
                        "document_id": p.document_id,
                        "board_position": p.board_position,
                        "political_party": p.political_party,
                        "election_period": p.election_period,
                        "presidency_type": p.presidency_type,
                        "position_time": p.position_time,
                        "institutional_email": p.institutional_email,
                        "digital_signature": p.digital_signature,
                        "fingerprint": p.fingerprint,
                        "created_at": str(p.created_at) if p.created_at else None,
                        "updated_at": str(p.updated_at) if p.updated_at else None,
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
        """POST /api/v1/municipal-council-presidents/ - Create a new president"""
        logger.info("=== VIEW: POST /api/v1/municipal-council-presidents/ ===")

        try:
            data = request.data

            president_dto = CreateMunicipalCouncilPresidentDTO(
                full_name=data.get("full_name", ""),
                document_type=data.get("document_type", ""),
                document_id=data.get("document_id", ""),
                board_position=data.get("board_position", ""),
                political_party=data.get("political_party", ""),
                election_period=data.get("election_period", ""),
                presidency_type=data.get("presidency_type", ""),
                position_time=data.get("position_time", ""),
                institutional_email=data.get("institutional_email", ""),
                digital_signature=data.get("digital_signature"),
                fingerprint=data.get("fingerprint"),
            )

            use_case = CreateMunicipalCouncilPresidentUseCase(self.repository)
            result = use_case.execute(president_dto)

            return Response(
                {
                    "success": True,
                    "message": "Presidente de consejo municipal creado exitosamente",
                    "data": {
                        "id": result.id,
                        "full_name": result.full_name,
                        "document_type": result.document_type,
                        "document_id": result.document_id,
                        "board_position": result.board_position,
                        "political_party": result.political_party,
                        "election_period": result.election_period,
                        "presidency_type": result.presidency_type,
                        "position_time": result.position_time,
                        "institutional_email": result.institutional_email,
                        "digital_signature": result.digital_signature,
                        "fingerprint": result.fingerprint,
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
class MunicipalCouncilPresidentDetailView(APIView):
    """View for getting, updating, deleting a specific president"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseMunicipalCouncilPresidentRepository()

    def _format_president(self, president):
        """Format president entity to dict"""
        return {
            "id": president.id,
            "full_name": president.full_name,
            "document_type": president.document_type,
            "document_id": president.document_id,
            "board_position": president.board_position,
            "political_party": president.political_party,
            "election_period": president.election_period,
            "presidency_type": president.presidency_type,
            "position_time": president.position_time,
            "institutional_email": president.institutional_email,
            "digital_signature": president.digital_signature,
            "fingerprint": president.fingerprint,
            "created_at": str(president.created_at) if president.created_at else None,
            "updated_at": str(president.updated_at) if president.updated_at else None,
        }

    def get(self, request, president_id):
        """GET /api/v1/municipal-council-presidents/{id}/ - Get a specific president"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-presidents/{president_id}/ ==="
        )

        try:
            use_case = GetMunicipalCouncilPresidentByIdUseCase(self.repository)
            president = use_case.execute(president_id)

            return Response(
                {"success": True, "data": self._format_president(president)},
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

    def put(self, request, president_id):
        """PUT /api/v1/municipal-council-presidents/{id}/ - Update a president"""
        logger.info(
            f"=== VIEW: PUT /api/v1/municipal-council-presidents/{president_id}/ ==="
        )

        try:
            data = request.data

            use_case = UpdateMunicipalCouncilPresidentUseCase(self.repository)
            president = use_case.execute(president_id, data)

            return Response(
                {
                    "success": True,
                    "message": "Presidente de consejo municipal actualizado exitosamente",
                    "data": self._format_president(president),
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

    def delete(self, request, president_id):
        """DELETE /api/v1/municipal-council-presidents/{id}/ - Delete a president"""
        logger.info(
            f"=== VIEW: DELETE /api/v1/municipal-council-presidents/{president_id}/ ==="
        )

        try:
            use_case = DeleteMunicipalCouncilPresidentUseCase(self.repository)
            use_case.execute(president_id)

            return Response(
                {
                    "success": True,
                    "message": "Presidente de consejo municipal eliminado exitosamente",
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
