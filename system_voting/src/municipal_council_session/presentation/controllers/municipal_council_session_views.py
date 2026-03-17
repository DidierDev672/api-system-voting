"""
Municipal Council Session Controllers
Presentation Layer - API Views
Vertical Slicing + Hexagonal Architecture
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from system_voting.src.municipal_council_session.domain.entities.municipal_council_session import (
    CreateMunicipalCouncilSessionDTO,
)
from system_voting.src.municipal_council_session.infrastructure.adapters.supabase_municipal_council_session_repository import (
    SupabaseMunicipalCouncilSessionRepository,
)
from system_voting.src.municipal_council_session.application.use_cases.municipal_council_session_use_cases import (
    CreateMunicipalCouncilSessionUseCase,
    GetAllMunicipalCouncilSessionsUseCase,
    GetMunicipalCouncilSessionByIdUseCase,
    UpdateMunicipalCouncilSessionUseCase,
    DeleteMunicipalCouncilSessionUseCase,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class MunicipalCouncilSessionListCreateView(APIView):
    """View for listing and creating municipal council sessions"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseMunicipalCouncilSessionRepository()

    def get(self, request):
        """GET /api/v1/municipal-council-sessions/ - Get all sessions"""
        logger.info("=== VIEW: GET /api/v1/municipal-council-sessions/ ===")

        try:
            use_case = GetAllMunicipalCouncilSessionsUseCase(self.repository)
            sessions = use_case.execute()

            data = []
            for s in sessions:
                data.append(
                    {
                        "id": s.id,
                        "title_session": s.title_session,
                        "type_session": s.type_session,
                        "status_session": s.status_session,
                        "date_hour_start": s.date_hour_start,
                        "date_hour_end": s.date_hour_end,
                        "modality": s.modality,
                        "place_enclosure": s.place_enclosure,
                        "orden_day": s.orden_day,
                        "quorum_required": s.quorum_required,
                        "id_president": s.id_president,
                        "id_secretary": s.id_secretary,
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
        """POST /api/v1/municipal-council-sessions/ - Create a new session"""
        logger.info("=== VIEW: POST /api/v1/municipal-council-sessions/ ===")

        try:
            data = request.data

            session_dto = CreateMunicipalCouncilSessionDTO(
                title_session=data.get("title_session", ""),
                type_session=data.get("type_session", ""),
                status_session=data.get("status_session", ""),
                date_hour_start=data.get("date_hour_start", ""),
                date_hour_end=data.get("date_hour_end", ""),
                modality=data.get("modality", ""),
                place_enclosure=data.get("place_enclosure", ""),
                orden_day=data.get("orden_day", ""),
                quorum_required=data.get("quorum_required", 0),
                id_president=data.get("id_president", ""),
                id_secretary=data.get("id_secretary", ""),
            )

            use_case = CreateMunicipalCouncilSessionUseCase(self.repository)
            result = use_case.execute(session_dto)

            return Response(
                {
                    "success": True,
                    "message": "Sesion de consejo municipal creada exitosamente",
                    "data": {
                        "id": result.id,
                        "title_session": result.title_session,
                        "type_session": result.type_session,
                        "status_session": result.status_session,
                        "date_hour_start": result.date_hour_start,
                        "date_hour_end": result.date_hour_end,
                        "modality": result.modality,
                        "place_enclosure": result.place_enclosure,
                        "orden_day": result.orden_day,
                        "quorum_required": result.quorum_required,
                        "id_president": result.id_president,
                        "id_secretary": result.id_secretary,
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
class MunicipalCouncilSessionDetailView(APIView):
    """View for getting, updating, deleting a specific session"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseMunicipalCouncilSessionRepository()

    def _format_session(self, session):
        """Format session entity to dict"""
        return {
            "id": session.id,
            "title_session": session.title_session,
            "type_session": session.type_session,
            "status_session": session.status_session,
            "date_hour_start": session.date_hour_start,
            "date_hour_end": session.date_hour_end,
            "modality": session.modality,
            "place_enclosure": session.place_enclosure,
            "orden_day": session.orden_day,
            "quorum_required": session.quorum_required,
            "id_president": session.id_president,
            "id_secretary": session.id_secretary,
            "created_at": str(session.created_at) if session.created_at else None,
            "updated_at": str(session.updated_at) if session.updated_at else None,
        }

    def get(self, request, session_id):
        """GET /api/v1/municipal-council-sessions/{id}/ - Get a specific session"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-sessions/{session_id}/ ==="
        )

        try:
            use_case = GetMunicipalCouncilSessionByIdUseCase(self.repository)
            session = use_case.execute(session_id)

            return Response(
                {"success": True, "data": self._format_session(session)},
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

    def put(self, request, session_id):
        """PUT /api/v1/municipal-council-sessions/{id}/ - Update a session"""
        logger.info(
            f"=== VIEW: PUT /api/v1/municipal-council-sessions/{session_id}/ ==="
        )

        try:
            data = request.data

            use_case = UpdateMunicipalCouncilSessionUseCase(self.repository)
            session = use_case.execute(session_id, data)

            return Response(
                {
                    "success": True,
                    "message": "Sesion de consejo municipal actualizada exitosamente",
                    "data": self._format_session(session),
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

    def delete(self, request, session_id):
        """DELETE /api/v1/municipal-council-sessions/{id}/ - Delete a session"""
        logger.info(
            f"=== VIEW: DELETE /api/v1/municipal-council-sessions/{session_id}/ ==="
        )

        try:
            use_case = DeleteMunicipalCouncilSessionUseCase(self.repository)
            use_case.execute(session_id)

            return Response(
                {
                    "success": True,
                    "message": "Sesion de consejo municipal eliminada exitosamente",
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
