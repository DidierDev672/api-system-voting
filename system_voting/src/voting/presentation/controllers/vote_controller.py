"""
Controlador de Votos - Presentación
Vertical Slicing + Hexagonal Architecture
"""

import json
import logging
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from system_voting.src.voting.domain.entities.vote import CreateVoteCommand
from system_voting.src.voting.application.usecases.register_vote import (
    RegisterVoteUseCase,
    GetVotesByConsultationUseCase,
    GetVotesByMemberUseCase,
)
from system_voting.src.voting.infrastructure.adapters.supabase_vote_repository import (
    SupabaseVoteRepository,
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class VoteCreateView(APIView):
    """Vista para crear un voto"""

    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vote_repository = SupabaseVoteRepository()

    def get(self, request):
        """Endpoint GET /api/vote/ - Verificar si un miembro ya votó en una consulta o obtener todos los votos"""
        member_id = request.query_params.get("member_id")
        consultation_id = request.query_params.get("consultation_id")

        # Si no hay parámetros, devolver todos los votos
        if not member_id and not consultation_id:
            try:
                votes = self.vote_repository.get_all()

                votes_data = []
                for vote in votes:
                    votes_data.append(
                        {
                            "id": vote.id,
                            "id_consult": vote.id_consult,
                            "id_member": vote.id_member,
                            "id_party": vote.id_party,
                            "id_auth": vote.id_auth,
                            "value_vote": vote.value_vote,
                            "comment": vote.comment,
                            "created_at": vote.created_at,
                        }
                    )

                return Response(
                    {"success": True, "data": votes_data, "count": len(votes_data)},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                logger.error(f"=== VIEW GET ALL ERROR: {str(e)} ===")
                return Response(
                    {"success": False, "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Si solo hay consultation_id, devolver votos de esa consulta
        if consultation_id and not member_id:
            try:
                votes = self.vote_repository.find_by_consultation(consultation_id)

                votes_data = []
                for vote in votes:
                    votes_data.append(
                        {
                            "id": vote.id,
                            "id_consult": vote.id_consult,
                            "id_member": vote.id_member,
                            "id_party": vote.id_party,
                            "id_auth": vote.id_auth,
                            "value_vote": vote.value_vote,
                            "comment": vote.comment,
                            "created_at": vote.created_at,
                        }
                    )

                return Response(
                    {"success": True, "data": votes_data, "count": len(votes_data)},
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                logger.error(f"=== VIEW GET BY CONSULTATION ERROR: {str(e)} ===")
                return Response(
                    {"success": False, "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Verificar si un miembro ya votó en una consulta específica
        if not member_id or not consultation_id:
            return Response(
                {
                    "success": False,
                    "error": "member_id y consultation_id son requeridos",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            use_case = GetVotesByMemberUseCase(self.vote_repository)
            result = use_case.execute(member_id)

            # Filtrar por consulta
            votes = [v for v in result["votes"] if v.id_consult == consultation_id]

            return Response(
                {
                    "success": True,
                    "has_voted": len(votes) > 0,
                    "vote": votes[0] if votes else None,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"=== VIEW GET ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        """Endpoint POST /api/vote/ - Registrar un nuevo voto"""
        logger.info("=== VIEW: POST /api/vote/ - Crear voto ===")

        try:
            data = request.data

            # Validar campos requeridos
            required_fields = [
                "id_consult",
                "id_member",
                "id_party",
                "id_auth",
                "value_vote",
            ]
            for field in required_fields:
                if field not in data:
                    return Response(
                        {"success": False, "error": f"El campo {field} es requerido"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Crear comando
            command = CreateVoteCommand(
                id_consult=str(data["id_consult"]),
                id_member=str(data["id_member"]),
                id_party=str(data["id_party"]),
                id_auth=str(data["id_auth"]),
                value_vote=bool(data["value_vote"]),
                comment=data.get("comment"),
            )

            # Ejecutar caso de uso
            use_case = RegisterVoteUseCase(self.vote_repository)
            result = use_case.execute(command)

            vote = result["vote"]

            return Response(
                {
                    "success": True,
                    "message": "Voto registrado exitosamente",
                    "data": {
                        "id": vote.id,
                        "id_consult": vote.id_consult,
                        "id_member": vote.id_member,
                        "id_party": vote.id_party,
                        "id_auth": vote.id_auth,
                        "value_vote": vote.value_vote,
                        "comment": vote.comment,
                        "created_at": vote.created_at,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as ve:
            logger.warning(f"=== VIEW: Validación fallida: {str(ve)} ===")
            return Response(
                {"success": False, "error": str(ve)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class VoteByConsultationView(APIView):
    """Vista para obtener votos de una consulta"""

    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vote_repository = SupabaseVoteRepository()

    def get(self, request, id_consult):
        """Endpoint GET /api/vote/consult/{id_consult}/ - Obtener votos de una consulta"""
        logger.info(f"=== VIEW: GET /api/vote/consult/{id_consult}/ ===")

        try:
            use_case = GetVotesByConsultationUseCase(self.vote_repository)
            result = use_case.execute(id_consult)

            votes_data = []
            for vote in result["votes"]:
                votes_data.append(
                    {
                        "id": vote.id,
                        "id_consult": vote.id_consult,
                        "id_member": vote.id_member,
                        "id_party": vote.id_party,
                        "id_auth": vote.id_auth,
                        "value_vote": vote.value_vote,
                        "comment": vote.comment,
                        "created_at": vote.created_at,
                    }
                )

            return Response(
                {"success": True, "data": votes_data, "count": result["count"]},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class VoteByMemberView(APIView):
    """Vista para obtener votos de un miembro"""

    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vote_repository = SupabaseVoteRepository()

    def get(self, request, id_member):
        """Endpoint GET /api/vote/member/{id_member}/ - Obtener votos de un miembro"""
        logger.info(f"=== VIEW: GET /api/vote/member/{id_member}/ ===")

        try:
            use_case = GetVotesByMemberUseCase(self.vote_repository)
            result = use_case.execute(id_member)

            votes_data = []
            for vote in result["votes"]:
                votes_data.append(
                    {
                        "id": vote.id,
                        "id_consult": vote.id_consult,
                        "id_member": vote.id_member,
                        "id_party": vote.id_party,
                        "id_auth": vote.id_auth,
                        "value_vote": vote.value_vote,
                        "comment": vote.comment,
                        "created_at": vote.created_at,
                    }
                )

            return Response(
                {"success": True, "data": votes_data, "count": result["count"]},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
