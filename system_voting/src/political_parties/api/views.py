from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from system_voting.src.political_parties.application.register_party.validator import (
    PoliticalPartyValidator,
)
from system_voting.src.political_parties.domain.entities.political_party import (
    PoliticalParty,
)
from system_voting.src.political_parties.domain.value_objects.party_type import (
    PartyType,
)
from supabase_integration import political_parties_service


class RegisterPoliticalPartyView(APIView):
    def post(self, request):
        try:
            # Convertir tipo de partido de español a inglés
            party_type_spanish = request.data.get("party_type", "")
            party_type_english = PartyType.from_spanish(party_type_spanish)

            # Crear copia de los datos con el tipo convertido
            data = dict(request.data)
            data["party_type"] = party_type_english

            # Validar los datos de entrada
            PoliticalPartyValidator.validate(data)

            # Crear la entidad PoliticalParty
            party = PoliticalParty(**data)

            # Preparar datos para Supabase
            party_data = {
                "name": party.name,
                "acronym": party.acronym,
                "party_type": party.party_type,
                "ideology": party.ideology,
                "legal_representative": party.legal_representative,
                "representative_id": party.representative_id,
                "email": party.email,
                "foundation_date": party.foundation_date,
                "is_active": party.is_active,
            }

            # Guardar en Supabase
            result = political_parties_service.create_party(party_data)

            return Response(
                {"message": "Partido político registrado exitosamente", "data": result},
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response(
                {"error": "Error de validación", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            import traceback

            print(f"Error en RegisterPoliticalPartyView: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {
                    "error": "Error interno del servidor",
                    "message": f"Ocurrió un error inesperado: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ListPoliticalPartiesView(APIView):
    def get(self, request):
        try:
            # Obtener partidos activos desde Supabase
            parties = political_parties_service.get_all_active_parties()

            return Response(
                {
                    "message": "Partidos políticos obtenidos exitosamente",
                    "data": parties,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "error": "Error interno del servidor",
                    "message": "Error al obtener los partidos políticos",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
