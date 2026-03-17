"""
Screening Controllers
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

from system_voting.src.screening.domain.entities.screening import CreateScreeningDTO
from system_voting.src.screening.infrastructure.adapters.supabase_screening_repository import (
    SupabaseScreeningRepository,
)
from system_voting.src.screening.application.use_cases.screening_use_cases import (
    CreateScreeningUseCase,
    GetAllScreeningsUseCase,
    GetScreeningByIdUseCase,
    UpdateScreeningUseCase,
    DeleteScreeningUseCase,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class ScreeningListCreateView(APIView):
    """View for listing and creating screenings"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseScreeningRepository()

    def get(self, request):
        """GET /api/v1/screenings/ - Get all screenings"""
        logger.info("=== VIEW: GET /api/v1/screenings/ ===")

        try:
            use_case = GetAllScreeningsUseCase(self.repository)
            screenings = use_case.execute()

            # Convert to dict response
            data = []
            for s in screenings:
                data.append(
                    {
                        "id": s.id,
                        "title": s.title,
                        "description": s.description,
                        "questions": [
                            {
                                "sound": q.sound,
                                "optionsAnswer": [
                                    {"id": opt.id, "text": opt.text, "value": opt.value}
                                    for opt in q.optionsAnswer
                                ],
                            }
                            for q in s.questions
                        ],
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
        """POST /api/v1/screenings/ - Create a new screening"""
        logger.info("=== VIEW: POST /api/v1/screenings/ ===")

        try:
            data = request.data

            screening_dto = CreateScreeningDTO(
                title=data.get("title", ""),
                description=data.get("description", ""),
                questions=data.get("questions", []),
            )

            use_case = CreateScreeningUseCase(self.repository)
            result = use_case.execute(screening_dto)

            return Response(
                {
                    "success": True,
                    "message": "Tamizaje creado exitosamente",
                    "data": {
                        "id": result.id,
                        "title": result.title,
                        "description": result.description,
                        "questions": [
                            {
                                "sound": q.sound,
                                "optionsAnswer": [
                                    {"id": opt.id, "text": opt.text, "value": opt.value}
                                    for opt in q.optionsAnswer
                                ],
                            }
                            for q in result.questions
                        ],
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
class ScreeningDetailView(APIView):
    """View for getting, updating, deleting a specific screening"""

    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = SupabaseScreeningRepository()

    def _format_screening(self, screening):
        """Format screening entity to dict"""
        return {
            "id": screening.id,
            "title": screening.title,
            "description": screening.description,
            "questions": [
                {
                    "sound": q.sound,
                    "optionsAnswer": [
                        {"id": opt.id, "text": opt.text, "value": opt.value}
                        for opt in q.optionsAnswer
                    ],
                }
                for q in screening.questions
            ],
            "created_at": str(screening.created_at) if screening.created_at else None,
            "updated_at": str(screening.updated_at) if screening.updated_at else None,
        }

    def get(self, request, screening_id):
        """GET /api/v1/screenings/{id}/ - Get a specific screening"""
        logger.info(f"=== VIEW: GET /api/v1/screenings/{screening_id}/ ===")

        try:
            use_case = GetScreeningByIdUseCase(self.repository)
            screening = use_case.execute(screening_id)

            return Response(
                {"success": True, "data": self._format_screening(screening)},
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

    def put(self, request, screening_id):
        """PUT /api/v1/screenings/{id}/ - Update a screening"""
        logger.info(f"=== VIEW: PUT /api/v1/screenings/{screening_id}/ ===")

        try:
            data = request.data

            use_case = UpdateScreeningUseCase(self.repository)
            screening = use_case.execute(screening_id, data)

            return Response(
                {
                    "success": True,
                    "message": "Tamizaje actualizado exitosamente",
                    "data": self._format_screening(screening),
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

    def delete(self, request, screening_id):
        """DELETE /api/v1/screenings/{id}/ - Delete a screening"""
        logger.info(f"=== VIEW: DELETE /api/v1/screenings/{screening_id}/ ===")

        try:
            use_case = DeleteScreeningUseCase(self.repository)
            use_case.execute(screening_id)

            return Response(
                {"success": True, "message": "Tamizaje eliminado exitosamente"},
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
