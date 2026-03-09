from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from system_voting.src.political_parties.application.register_party.validator import PoliticalPartyValidator
from system_voting.src.political_parties.domain.entities.political_party import PoliticalParty
from supabase_integration.services import political_parties_service


class RegisterPoliticalPartyView(APIView):

    def post(self, request):
        try:
            # Validar los datos de entrada
            PoliticalPartyValidator.validate(request.data)
            
            # Crear la entidad PoliticalParty
            party = PoliticalParty(**request.data)
            
            # Preparar datos para Supabase
            party_data = {
                "name": party.name,
                "acronym": party.acronym,
                "party_type": party.party_type,
                "ideology": party.ideology,
                "legal_representative": party.legal_representative,
                "representative_id": party.representative_id,
                "email": party.email,
                "foundation_date": party.foundation_date
            }
            
            # Guardar en Supabase
            result = political_parties_service.create_party(party_data)
            
            return Response({ 
                "message": "Partido político registrado exitosamente",
                "data": result
            }, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response({ 
                "error": "Error de validación", 
                "message": str(e) 
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({ 
                "error": "Error interno del servidor", 
                "message": "Ocurrió un error inesperado al procesar la solicitud" 
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListPoliticalPartiesView(APIView):
    
    def get(self, request):
        try:
            # Obtener partidos activos desde Supabase
            parties = political_parties_service.get_all_active_parties()
            
            return Response({
                "message": "Partidos políticos obtenidos exitosamente",
                "data": parties
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ 
                "error": "Error interno del servidor", 
                "message": "Error al obtener los partidos políticos" 
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)