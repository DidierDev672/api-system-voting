"""
Adaptador de Salida para Votos - Supabase
Vertical Slicing + Hexagonal Architecture
"""

import logging
import uuid
from typing import List, Optional, Dict, Any
from supabase_integration.services import SupabaseService
from system_voting.src.voting.domain.entities.vote import Vote
from system_voting.src.voting.domain.ports.vote_repository import VoteRepositoryPort

logger = logging.getLogger(__name__)


class SupabaseVoteRepository(VoteRepositoryPort):
    """Adaptador que implementa el puerto usando Supabase"""

    def __init__(self):
        self.supabase_service = SupabaseService()
        self.table_name = "votes_consult"

    def save(self, vote: Vote) -> Vote:
        """Persistir un nuevo voto en Supabase"""
        logger.info(f"=== ADAPTER: Guardando voto para consulta {vote.id_consult} ===")

        vote_id = str(uuid.uuid4())

        vote_data = {
            "id": vote_id,
            "id_consult": vote.id_consult,
            "id_member": vote.id_member,
            "id_party": vote.id_party,
            "id_auth": vote.id_auth,
            "value_vote": vote.value_vote,
            "comment": vote.comment,
        }

        result = self.supabase_service.insert_record(self.table_name, vote_data)

        logger.info(f"=== ADAPTER: Voto guardado: {result} ===")

        return self._map_to_entity(result)

    def find_by_id(self, vote_id: str) -> Optional[Vote]:
        """Obtener voto por ID"""
        logger.info(f"=== ADAPTER: Buscando voto por ID: {vote_id} ===")

        result = self.supabase_service.get_record_by_id(self.table_name, vote_id)

        if not result:
            return None

        return self._map_to_entity(result)

    def find_by_consultation(self, id_consult: str) -> List[Vote]:
        """Obtener todos los votos de una consulta"""
        logger.info(f"=== ADAPTER: Buscando votos para consulta: {id_consult} ===")

        results = self.supabase_service.get_all_records(
            self.table_name, {"id_consult": id_consult}
        )

        logger.info(
            f"=== ADAPTER: {len(results) if results else 0} votos encontrados ==="
        )

        return [self._map_to_entity(r) for r in (results or [])]

    def find_by_member(self, id_member: str) -> List[Vote]:
        """Obtener todos los votos de un miembro"""
        logger.info(f"=== ADAPTER: Buscando votos para miembro: {id_member} ===")

        results = self.supabase_service.get_all_records(
            self.table_name, {"id_member": id_member}
        )

        logger.info(
            f"=== ADAPTER: {len(results) if results else 0} votos encontrados ==="
        )

        return [self._map_to_entity(r) for r in (results or [])]

    def get_all(self) -> List[Vote]:
        """Obtener todos los votos"""
        logger.info("=== ADAPTER: Obteniendo todos los votos ===")

        results = self.supabase_service.get_all_records(self.table_name, {})

        logger.info(
            f"=== ADAPTER: {len(results) if results else 0} votos encontrados en total ==="
        )

        return [self._map_to_entity(r) for r in (results or [])]

    def exists_by_member_and_consult(self, id_member: str, id_consult: str) -> bool:
        """Verificar si un miembro ya votó en una consulta"""
        logger.info(
            f"=== ADAPTER: Verificando si miembro {id_member} ya votó en consulta {id_consult} ==="
        )

        results = self.supabase_service.get_all_records(
            self.table_name, {"id_member": id_member, "id_consult": id_consult}
        )

        exists = len(results) > 0 if results else False

        logger.info(f"=== ADAPTER: Resultado: {exists} ===")

        return exists

    def delete(self, vote_id: str) -> bool:
        """Eliminar un voto"""
        logger.info(f"=== ADAPTER: Eliminando voto: {vote_id} ===")

        result = self.supabase_service.delete_record(self.table_name, vote_id)

        logger.info(f"=== ADAPTER: Voto eliminado: {result} ===")

        return result

    def _map_to_entity(self, data: Dict[str, Any]) -> Vote:
        """Mapear datos de Supabase a entidad de dominio"""
        return Vote(
            id=data.get("id"),
            id_consult=data.get("id_consult", ""),
            id_member=data.get("id_member", ""),
            id_party=data.get("id_party", ""),
            id_auth=data.get("id_auth", ""),
            value_vote=data.get("value_vote", False),
            comment=data.get("comment"),
            created_at=data.get("created_at"),
        )
