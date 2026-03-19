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
from supabase import create_client
import os

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

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
supabase_client = (
    create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None
)


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
                session_data = {
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
                    "members": [],
                    "bancadas": [],
                }

                if supabase_client:
                    try:
                        # Get session members (without join - query separately)
                        members_response = (
                            supabase_client.table("session_members")
                            .select("*")
                            .eq("id_session", s.id)
                            .execute()
                        )

                        members_list = []
                        for item in members_response.data:
                            # Get member details separately
                            member_id = item.get("id_member")
                            member_name = ""
                            member_document = ""
                            member_email = ""

                            if member_id:
                                try:
                                    member_response = (
                                        supabase_client.table("party_members")
                                        .select("full_name, document_number, email")
                                        .eq("id", member_id)
                                        .execute()
                                    )
                                    if member_response.data:
                                        member_name = member_response.data[0].get(
                                            "full_name", ""
                                        )
                                        member_document = member_response.data[0].get(
                                            "document_number", ""
                                        )
                                        member_email = member_response.data[0].get(
                                            "email", ""
                                        )
                                except Exception as e:
                                    logger.warning(
                                        f"Error getting member details: {str(e)}"
                                    )

                            members_list.append(
                                {
                                    "id": item.get("id"),
                                    "id_member": member_id,
                                    "member_name": member_name,
                                    "member_document": member_document,
                                    "member_email": member_email,
                                    "is_present": item.get("is_present", False),
                                    "arrival_time": item.get("arrival_time"),
                                }
                            )
                        session_data["members"] = members_list

                        # Get session bancadas (without join - query separately)
                        bancadas_response = (
                            supabase_client.table("session_bancadas")
                            .select("*")
                            .eq("id_session", s.id)
                            .execute()
                        )

                        bancadas_list = []
                        for item in bancadas_response.data:
                            # Get bancada details separately
                            bancada_id = item.get("id_bancada")
                            bancada_tipo_curul = ""
                            bancada_profesion = ""
                            bancada_correo = ""

                            if bancada_id:
                                try:
                                    bancada_response = (
                                        supabase_client.table("bancada")
                                        .select(
                                            "tipo_curul, profesion, correo_institucional"
                                        )
                                        .eq("id", bancada_id)
                                        .execute()
                                    )
                                    if bancada_response.data:
                                        bancada_tipo_curul = bancada_response.data[
                                            0
                                        ].get("tipo_curul", "")
                                        bancada_profesion = bancada_response.data[
                                            0
                                        ].get("profesion", "")
                                        bancada_correo = bancada_response.data[0].get(
                                            "correo_institucional", ""
                                        )
                                except Exception as e:
                                    logger.warning(
                                        f"Error getting bancada details: {str(e)}"
                                    )

                            bancadas_list.append(
                                {
                                    "id": item.get("id"),
                                    "id_bancada": bancada_id,
                                    "bancada_tipo_curul": bancada_tipo_curul,
                                    "bancada_profesion": bancada_profesion,
                                    "bancada_correo": bancada_correo,
                                }
                            )
                        session_data["bancadas"] = bancadas_list

                    except Exception as e:
                        logger.warning(
                            f"=== Error loading session relations: {str(e)} ==="
                        )

                data.append(session_data)

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

    def _format_session(self, session, include_relations=True):
        """Format session entity to dict with optional members and bancadas"""
        data = {
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

        if include_relations and supabase_client:
            try:
                # Get session members (without join)
                members_response = (
                    supabase_client.table("session_members")
                    .select("*")
                    .eq("id_session", session.id)
                    .execute()
                )

                members_data = []
                for item in members_response.data:
                    member_id = item.get("id_member")
                    member_name = ""
                    member_document = ""
                    member_email = ""

                    if member_id:
                        try:
                            member_response = (
                                supabase_client.table("party_members")
                                .select("full_name, document_number, email")
                                .eq("id", member_id)
                                .execute()
                            )
                            if member_response.data:
                                member_name = member_response.data[0].get(
                                    "full_name", ""
                                )
                                member_document = member_response.data[0].get(
                                    "document_number", ""
                                )
                                member_email = member_response.data[0].get("email", "")
                        except Exception as e:
                            logger.warning(f"Error getting member details: {str(e)}")

                    members_data.append(
                        {
                            "id": item.get("id"),
                            "id_member": member_id,
                            "member_name": member_name,
                            "member_document": member_document,
                            "member_email": member_email,
                            "is_present": item.get("is_present", False),
                            "arrival_time": item.get("arrival_time"),
                        }
                    )
                data["members"] = members_data

                # Get session bancadas (without join)
                bancadas_response = (
                    supabase_client.table("session_bancadas")
                    .select("*")
                    .eq("id_session", session.id)
                    .execute()
                )

                bancadas_data = []
                for item in bancadas_response.data:
                    bancada_id = item.get("id_bancada")
                    bancada_tipo_curul = ""
                    bancada_profesion = ""
                    bancada_correo = ""

                    if bancada_id:
                        try:
                            bancada_response = (
                                supabase_client.table("bancada")
                                .select("tipo_curul, profesion, correo_institucional")
                                .eq("id", bancada_id)
                                .execute()
                            )
                            if bancada_response.data:
                                bancada_tipo_curul = bancada_response.data[0].get(
                                    "tipo_curul", ""
                                )
                                bancada_profesion = bancada_response.data[0].get(
                                    "profesion", ""
                                )
                                bancada_correo = bancada_response.data[0].get(
                                    "correo_institucional", ""
                                )
                        except Exception as e:
                            logger.warning(f"Error getting bancada details: {str(e)}")

                    bancadas_data.append(
                        {
                            "id": item.get("id"),
                            "id_bancada": bancada_id,
                            "bancada_tipo_curul": bancada_tipo_curul,
                            "bancada_profesion": bancada_profesion,
                            "bancada_correo": bancada_correo,
                        }
                    )
                data["bancadas"] = bancadas_data

            except Exception as e:
                logger.warning(f"=== Error loading session relations: {str(e)} ===")
                data["members"] = []
                data["bancadas"] = []
        else:
            data["members"] = []
            data["bancadas"] = []

        return data

    def get(self, request, session_id):
        """GET /api/v1/municipal-council-sessions/{id}/ - Get a specific session"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-sessions/{session_id}/ ==="
        )

        try:
            use_case = GetMunicipalCouncilSessionByIdUseCase(self.repository)
            session = use_case.execute(session_id)

            return Response(
                {
                    "success": True,
                    "data": self._format_session(session, include_relations=True),
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
                    "data": self._format_session(session, include_relations=True),
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


@method_decorator(csrf_exempt, name="dispatch")
class SessionMemberView(APIView):
    """View for managing members in a session"""

    permission_classes = []

    def get(self, request, session_id):
        """GET /api/v1/municipal-council-sessions/{session_id}/members/ - Get all members of a session"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-sessions/{session_id}/members/ ==="
        )

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Get session members without join
            response = (
                supabase_client.table("session_members")
                .select("*")
                .eq("id_session", session_id)
                .execute()
            )

            members_data = []
            for item in response.data:
                member_id = item.get("id_member")
                member_name = ""
                member_document = ""

                if member_id:
                    try:
                        member_response = (
                            supabase_client.table("party_members")
                            .select("full_name, document_number")
                            .eq("id", member_id)
                            .execute()
                        )
                        if member_response.data:
                            member_name = member_response.data[0].get("full_name", "")
                            member_document = member_response.data[0].get(
                                "document_number", ""
                            )
                    except Exception as e:
                        logger.warning(f"Error getting member: {str(e)}")

                members_data.append(
                    {
                        "id": item.get("id"),
                        "id_session": item.get("id_session"),
                        "id_member": member_id,
                        "member_name": member_name,
                        "member_document": member_document,
                        "is_present": item.get("is_present", False),
                        "arrival_time": item.get("arrival_time"),
                        "created_at": item.get("created_at"),
                    }
                )

            return Response(
                {"success": True, "data": members_data, "count": len(members_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, session_id):
        """POST /api/v1/municipal-council-sessions/{session_id}/members/ - Add member to session"""
        logger.info(
            f"=== VIEW: POST /api/v1/municipal-council-sessions/{session_id}/members/ ==="
        )
        logger.info(f"Request data: {request.data}")

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            data = request.data
            logger.info(f"Data received: {data}")
            id_member = data.get("id_member")
            logger.info(f"id_member extracted: {id_member}")

            if not id_member:
                return Response(
                    {"success": False, "error": "El ID del miembro es requerido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            existing = (
                supabase_client.table("session_members")
                .select("id")
                .eq("id_session", session_id)
                .eq("id_member", id_member)
                .execute()
            )

            if existing.data:
                return Response(
                    {
                        "success": False,
                        "error": "El miembro ya esta registrado en esta sesion",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_member = {
                "id_session": session_id,
                "id_member": id_member,
                "is_present": False,
            }

            logger.info(f"Inserting member with data: {new_member}")
            response = (
                supabase_client.table("session_members").insert(new_member).execute()
            )
            logger.info(f"Insert response: {response}")

            return Response(
                {
                    "success": True,
                    "message": "Miembro agregado a la sesion exitosamente",
                    "data": response.data[0] if response.data else new_member,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, session_id):
        """DELETE /api/v1/municipal-council-sessions/{session_id}/members/ - Remove member from session"""
        logger.info(
            f"=== VIEW: DELETE /api/v1/municipal-council-sessions/{session_id}/members/ ==="
        )

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            member_id = request.data.get("member_id") or request.query_params.get(
                "member_id"
            )

            if not member_id:
                return Response(
                    {"success": False, "error": "El ID del miembro es requerido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            supabase_client.table("session_members").delete().eq(
                "id_session", session_id
            ).eq("id_member", member_id).execute()

            return Response(
                {
                    "success": True,
                    "message": "Miembro removido de la sesion exitosamente",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class SessionBancadaView(APIView):
    """View for managing bancadas in a session"""

    permission_classes = []

    def get(self, request, session_id):
        """GET /api/v1/municipal-council-sessions/{session_id}/bancadas/ - Get all bancadas of a session"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-sessions/{session_id}/bancadas/ ==="
        )

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Get session bancadas without join
            response = (
                supabase_client.table("session_bancadas")
                .select("*")
                .eq("id_session", session_id)
                .execute()
            )

            bancadas_data = []
            for item in response.data:
                bancada_id = item.get("id_bancada")
                bancada_tipo_curul = ""
                bancada_profesion = ""

                if bancada_id:
                    try:
                        bancada_response = (
                            supabase_client.table("bancada")
                            .select("tipo_curul, profesion")
                            .eq("id", bancada_id)
                            .execute()
                        )
                        if bancada_response.data:
                            bancada_tipo_curul = bancada_response.data[0].get(
                                "tipo_curul", ""
                            )
                            bancada_profesion = bancada_response.data[0].get(
                                "profesion", ""
                            )
                    except Exception as e:
                        logger.warning(f"Error getting bancada: {str(e)}")

                bancadas_data.append(
                    {
                        "id": item.get("id"),
                        "id_session": item.get("id_session"),
                        "id_bancada": bancada_id,
                        "bancada_tipo_curul": bancada_tipo_curul,
                        "bancada_profesion": bancada_profesion,
                        "created_at": item.get("created_at"),
                    }
                )

            return Response(
                {"success": True, "data": bancadas_data, "count": len(bancadas_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, session_id):
        """POST /api/v1/municipal-council-sessions/{session_id}/bancadas/ - Add bancada to session"""
        logger.info(
            f"=== VIEW: POST /api/v1/municipal-council-sessions/{session_id}/bancadas/ ==="
        )
        logger.info(f"Request data: {request.data}")

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            data = request.data
            logger.info(f"Data received: {data}")
            id_bancada = data.get("id_bancada")
            logger.info(f"id_bancada extracted: {id_bancada}")

            if not id_bancada:
                return Response(
                    {"success": False, "error": "El ID de la bancada es requerido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            existing = (
                supabase_client.table("session_bancadas")
                .select("id")
                .eq("id_session", session_id)
                .eq("id_bancada", id_bancada)
                .execute()
            )

            if existing.data:
                return Response(
                    {
                        "success": False,
                        "error": "La bancada ya esta registrada en esta sesion",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_bancada = {
                "id_session": session_id,
                "id_bancada": id_bancada,
            }

            logger.info(f"Inserting bancada with data: {new_bancada}")
            response = (
                supabase_client.table("session_bancadas").insert(new_bancada).execute()
            )
            logger.info(f"Insert response: {response}")

            return Response(
                {
                    "success": True,
                    "message": "Bancada agregada a la sesion exitosamente",
                    "data": response.data[0] if response.data else new_bancada,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, session_id):
        """DELETE /api/v1/municipal-council-sessions/{session_id}/bancadas/ - Remove bancada from session"""
        logger.info(
            f"=== VIEW: DELETE /api/v1/municipal-council-sessions/{session_id}/bancadas/ ==="
        )

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            bancada_id = request.data.get("bancada_id") or request.query_params.get(
                "bancada_id"
            )

            if not bancada_id:
                return Response(
                    {"success": False, "error": "El ID de la bancada es requerido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            supabase_client.table("session_bancadas").delete().eq(
                "id_session", session_id
            ).eq("id_bancada", bancada_id).execute()

            return Response(
                {
                    "success": True,
                    "message": "Bancada removida de la sesion exitosamente",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class SessionAvailableMembersView(APIView):
    """View for getting available members that can be added to a session"""

    permission_classes = []

    def get(self, request, session_id):
        """GET /api/v1/municipal-council-sessions/{session_id}/members/available/ - Get available members to add"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-sessions/{session_id}/members/available/ ==="
        )

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            session_members = (
                supabase_client.table("session_members")
                .select("id_member")
                .eq("id_session", session_id)
                .execute()
            )

            assigned_member_ids = [m["id_member"] for m in session_members.data]

            if assigned_member_ids:
                response = (
                    supabase_client.table("party_members")
                    .select("id, full_name, document_number, email")
                    .not_in("id", assigned_member_ids)
                    .execute()
                )
            else:
                response = (
                    supabase_client.table("party_members")
                    .select("id, full_name, document_number, email")
                    .execute()
                )

            members_data = []
            for item in response.data:
                members_data.append(
                    {
                        "id": item.get("id"),
                        "full_name": item.get("full_name"),
                        "document_number": item.get("document_number"),
                        "email": item.get("email"),
                    }
                )

            return Response(
                {"success": True, "data": members_data, "count": len(members_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class SessionAvailableBancadasView(APIView):
    """View for getting available bancadas that can be added to a session"""

    permission_classes = []

    def get(self, request, session_id):
        """GET /api/v1/municipal-council-sessions/{session_id}/bancadas/available/ - Get available bancadas to add"""
        logger.info(
            f"=== VIEW: GET /api/v1/municipal-council-sessions/{session_id}/bancadas/available/ ==="
        )

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            session_bancadas = (
                supabase_client.table("session_bancadas")
                .select("id_bancada")
                .eq("id_session", session_id)
                .execute()
            )

            assigned_bancada_ids = [b["id_bancada"] for b in session_bancadas.data]

            if assigned_bancada_ids:
                response = (
                    supabase_client.table("bancada")
                    .select("id, tipo_curul, profesion, correo_institucional")
                    .not_in("id", assigned_bancada_ids)
                    .execute()
                )
            else:
                response = (
                    supabase_client.table("bancada")
                    .select("id, tipo_curul, profesion, correo_institucional")
                    .execute()
                )

            bancadas_data = []
            for item in response.data:
                bancadas_data.append(
                    {
                        "id": item.get("id"),
                        "tipo_curul": item.get("tipo_curul"),
                        "profesion": item.get("profesion"),
                        "correo_institucional": item.get("correo_institucional"),
                    }
                )

            return Response(
                {"success": True, "data": bancadas_data, "count": len(bancadas_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class AllMembersView(APIView):
    """View for getting all party members in the system"""

    permission_classes = []

    def get(self, request):
        """GET /api/v1/municipal-council-sessions/members/ - Get all party members"""
        logger.info("=== VIEW: GET /api/v1/municipal-council-sessions/members/ ===")

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response = (
                supabase_client.table("party_members")
                .select("id, full_name, document_number")
                .order("full_name")
                .execute()
            )

            members_data = []
            for item in response.data:
                members_data.append(
                    {
                        "id": item.get("id"),
                        "full_name": item.get("full_name"),
                        "document_number": item.get("document_number"),
                    }
                )

            return Response(
                {"success": True, "data": members_data, "count": len(members_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@method_decorator(csrf_exempt, name="dispatch")
class AllBancadasView(APIView):
    """View for getting all bancadas in the system"""

    permission_classes = []

    def get(self, request):
        """GET /api/v1/municipal-council-sessions/bancadas/ - Get all bancadas"""
        logger.info("=== VIEW: GET /api/v1/municipal-council-sessions/bancadas/ ===")

        try:
            if not supabase_client:
                return Response(
                    {"success": False, "error": "Supabase no configurado"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response = (
                supabase_client.table("bancada")
                .select("id, tipo_curul, profesion, correo_institucional")
                .execute()
            )

            bancadas_data = []
            for item in response.data:
                bancadas_data.append(
                    {
                        "id": item.get("id"),
                        "tipo_curul": item.get("tipo_curul"),
                        "profesion": item.get("profesion"),
                        "correo_institucional": item.get("correo_institucional"),
                    }
                )

            return Response(
                {"success": True, "data": bancadas_data, "count": len(bancadas_data)},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
