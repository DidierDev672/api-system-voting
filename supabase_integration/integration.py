"""
Integración de Supabase con los repositorios existentes
Este archivo muestra cómo migrar los repositorios Django a Supabase
"""

from system_voting.src.party_members.domain.ports.party_member_repository import PartyMemberRepository
from system_voting.src.party_members.domain.entities.party_member import PartyMember
from supabase.services import party_members_service
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class SupabasePartyMemberRepository(PartyMemberRepository):
    """Implementación del repositorio de miembros usando Supabase"""
    
    def save(self, party_member: PartyMember) -> PartyMember:
        """Guardar un miembro de partido en Supabase"""
        try:
            member_data = {
                "full_name": party_member.full_name,
                "document_type": party_member.document_type,
                "document_number": party_member.document_number,
                "birth_date": party_member.birth_date,
                "city": party_member.city,
                "political_party_id": party_member.political_party_id,
                "consent": party_member.consent,
                "data_authorization": party_member.data_authorization,
                "affiliation_date": party_member.affiliation_date
            }
            
            result = party_members_service.create_member(member_data)
            
            # Actualizar el objeto PartyMember con el ID generado
            party_member.id = result["id"]
            party_member.created_at = result["created_at"]
            
            logger.info(f"Miembro {party_member.full_name} guardado en Supabase")
            return party_member
            
        except Exception as e:
            logger.error(f"Error guardando miembro en Supabase: {str(e)}")
            raise
    
    def get_all(self) -> List[dict]:
        """Obtener todos los miembros de partidos"""
        try:
            return party_members_service.get_all_records("party_members")
        except Exception as e:
            logger.error(f"Error obteniendo miembros de Supabase: {str(e)}")
            raise
    
    def get_by_id(self, member_id: str) -> Optional[dict]:
        """Obtener un miembro por ID"""
        try:
            return party_members_service.get_record_by_id("party_members", member_id)
        except Exception as e:
            logger.error(f"Error obteniendo miembro {member_id} de Supabase: {str(e)}")
            raise
    
    def get_by_document(self, document_number: str) -> Optional[dict]:
        """Obtener un miembro por número de documento"""
        try:
            return party_members_service.get_member_by_document(document_number)
        except Exception as e:
            logger.error(f"Error obteniendo miembro por documento {document_number}: {str(e)}")
            raise
    
    def get_by_party(self, political_party_id: str) -> List[dict]:
        """Obtener miembros por partido político"""
        try:
            return party_members_service.get_members_by_party(political_party_id)
        except Exception as e:
            logger.error(f"Error obteniendo miembros del partido {political_party_id}: {str(e)}")
            raise
    
    def update(self, member_id: str, data: dict) -> Optional[dict]:
        """Actualizar un miembro"""
        try:
            return party_members_service.update_record("party_members", member_id, data)
        except Exception as e:
            logger.error(f"Error actualizando miembro {member_id}: {str(e)}")
            raise
    
    def delete(self, member_id: str) -> bool:
        """Eliminar un miembro"""
        try:
            return party_members_service.delete_record("party_members", member_id)
        except Exception as e:
            logger.error(f"Error eliminando miembro {member_id}: {str(e)}")
            raise


# Similar para Political Parties
from system_voting.src.political_parties.domain.ports.party_repository import PoliticalPartyRepository
from system_voting.src.political_parties.domain.entities.political_party import PoliticalParty
from supabase.services import political_parties_service

class SupabasePoliticalPartyRepository(PoliticalPartyRepository):
    """Implementación del repositorio de partidos usando Supabase"""
    
    def save(self, party: PoliticalParty) -> PoliticalParty:
        """Guardar un partido político en Supabase"""
        try:
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
            
            result = political_parties_service.create_party(party_data)
            
            # Actualizar el objeto PoliticalParty con el ID generado
            party.id = result["id"]
            party.created_at = result["created_at"]
            
            logger.info(f"Partido {party.name} guardado en Supabase")
            return party
            
        except Exception as e:
            logger.error(f"Error guardando partido en Supabase: {str(e)}")
            raise
    
    def get_all(self) -> List[dict]:
        """Obtener todos los partidos políticos activos"""
        try:
            return political_parties_service.get_all_active_parties()
        except Exception as e:
            logger.error(f"Error obteniendo partidos de Supabase: {str(e)}")
            raise
    
    def get_by_id(self, party_id: str) -> Optional[dict]:
        """Obtener un partido por ID"""
        try:
            return political_parties_service.get_record_by_id("political_parties", party_id)
        except Exception as e:
            logger.error(f"Error obteniendo partido {party_id} de Supabase: {str(e)}")
            raise
    
    def get_by_name(self, name: str) -> Optional[dict]:
        """Obtener un partido por nombre"""
        try:
            return political_parties_service.get_party_by_name(name)
        except Exception as e:
            logger.error(f"Error obteniendo partido por nombre {name}: {str(e)}")
            raise
    
    def update(self, party_id: str, data: dict) -> Optional[dict]:
        """Actualizar un partido"""
        try:
            return political_parties_service.update_record("political_parties", party_id, data)
        except Exception as e:
            logger.error(f"Error actualizando partido {party_id}: {str(e)}")
            raise
    
    def delete(self, party_id: str) -> bool:
        """Eliminar un partido (desactivar)"""
        try:
            # En lugar de eliminar, desactivamos
            return political_parties_service.update_record("political_parties", party_id, {"is_active": False})
        except Exception as e:
            logger.error(f"Error desactivando partido {party_id}: {str(e)}")
            raise
    
    def get_statistics(self) -> List[dict]:
        """Obtener estadísticas de partidos"""
        try:
            return political_parties_service.get_party_statistics()
        except Exception as e:
            logger.error(f"Error obteniendo estadísticas de partidos: {str(e)}")
            raise


# Configuración para cambiar entre repositorios Django y Supabase
def get_party_member_repository(use_supabase: bool = True):
    """Factory para obtener el repositorio de miembros"""
    if use_supabase:
        return SupabasePartyMemberRepository()
    else:
        from system_voting.src.party_members.infrastructure.repositories import DjangoPartyMemberRepository
        return DjangoPartyMemberRepository()

def get_political_party_repository(use_supabase: bool = True):
    """Factory para obtener el repositorio de partidos"""
    if use_supabase:
        return SupabasePoliticalPartyRepository()
    else:
        from system_voting.src.political_parties.infrastructure.repositories import DjangoPoliticalPartyRepository
        return DjangoPoliticalPartyRepository()


# Ejemplo de cómo usar en los handlers
"""
En lugar de:
handler = RegisterPartyMemberHandler(DjangoPartyMemberRepository())

Usar:
handler = RegisterPartyMemberHandler(get_party_member_repository(use_supabase=True))

O configurar en settings.py:
USE_SUPABASE = os.getenv("USE_SUPABASE", "true").lower() == "true"

Y en los handlers:
from system_voting.src.infrastructure.supabase_integration import get_party_member_repository
from django.conf import settings

handler = RegisterPartyMemberHandler(
    get_party_member_repository(use_supabase=settings.USE_SUPABASE)
)
"""
