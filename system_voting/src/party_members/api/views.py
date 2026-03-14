from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from system_voting.src.party_members.application.register_member.validator import (
    PartyMemberValidator,
)
from system_voting.src.party_members.domain.entities.party_member import PartyMember
from supabase_integration.services import party_members_service


class RegisterPartyMemberView(APIView):
    def post(self, request):
        try:
            # Validar los datos de entrada
            PartyMemberValidator.validate(request.data)

            # Crear la entidad PartyMember
            member = PartyMember(**request.data)

            # Preparar datos para Supabase
            member_data = {
                "full_name": member.full_name,
                "document_type": member.document_type,
                "document_number": member.document_number,
                "birth_date": member.birth_date,
                "city": member.city,
                "political_party_id": member.political_party_id,
                "consent": member.consent,
                "data_authorization": member.data_authorization,
                "affiliation_date": member.affiliation_date,
            }

            # Guardar en Supabase
            result = party_members_service.create_member(member_data)

            return Response(
                {"message": "Afiliación registrada exitosamente", "data": result},
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {"error": "Error de validación", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "error": "Error interno del servidor",
                    "message": "Ocurrió un error inesperado al procesar la solicitud",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListPartyMembersView(APIView):
    def get(self, request):
        try:
            document_number = request.query_params.get("document_number")

            if document_number:
                member = party_members_service.get_member_by_document(document_number)
                members = [member] if member else []
            else:
                members = party_members_service.get_all_active_members()

            return Response(
                {
                    "message": "Miembros de partido obtenidos exitosamente",
                    "data": members,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            import traceback

            print(f"Error en ListPartyMembersView: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {
                    "error": "Error interno del servidor",
                    "message": f"Error al obtener los miembros de partido: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
