"""
Repository Adapter - Municipal Council President
Infrastructure Layer - Supabase Implementation
"""

import uuid
import logging
from typing import List, Optional
from supabase_integration import SupabaseService as BaseSupabaseService
from system_voting.src.municipal_council_president.domain.entities.municipal_council_president import (
    MunicipalCouncilPresident,
    CreateMunicipalCouncilPresidentDTO,
)
from system_voting.src.municipal_council_president.domain.ports.municipal_council_president_repository import (
    MunicipalCouncilPresidentRepositoryPort,
)

logger = logging.getLogger(__name__)


class SupabaseMunicipalCouncilPresidentRepository(
    MunicipalCouncilPresidentRepositoryPort
):
    """Supabase implementation of MunicipalCouncilPresidentRepositoryPort"""

    def __init__(self):
        self.supabase_service = BaseSupabaseService()
        self.table_name = "municipal_council_presidents"

    def _map_to_entity(self, data: dict) -> MunicipalCouncilPresident:
        """Map database response to MunicipalCouncilPresident entity"""
        return MunicipalCouncilPresident(
            id=data.get("id", ""),
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
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def create(
        self, president_data: CreateMunicipalCouncilPresidentDTO
    ) -> MunicipalCouncilPresident:
        """Create a new municipal council president"""
        logger.info(
            f"=== REPOSITORY: Creating municipal council president: {president_data.full_name} ==="
        )

        president_id = str(uuid.uuid4())

        data = {
            "id": president_id,
            "full_name": president_data.full_name,
            "document_type": president_data.document_type,
            "document_id": president_data.document_id,
            "board_position": president_data.board_position,
            "political_party": president_data.political_party,
            "election_period": president_data.election_period,
            "presidency_type": president_data.presidency_type,
            "position_time": president_data.position_time,
            "institutional_email": president_data.institutional_email,
            "digital_signature": president_data.digital_signature,
            "fingerprint": president_data.fingerprint,
        }

        result = self.supabase_service.insert_record(self.table_name, data)
        logger.info(
            f"=== REPOSITORY: Municipal council president created: {result} ==="
        )

        return self._map_to_entity(result)

    def get_all(self) -> List[MunicipalCouncilPresident]:
        """Get all municipal council presidents"""
        logger.info("=== REPOSITORY: Getting all municipal council presidents ===")

        results = self.supabase_service.get_all_records(self.table_name, {})

        presidents = [self._map_to_entity(r) for r in (results or [])]
        logger.info(f"=== REPOSITORY: Found {len(presidents)} presidents ===")

        return presidents

    def get_by_id(self, president_id: str) -> Optional[MunicipalCouncilPresident]:
        """Get municipal council president by ID"""
        logger.info(
            f"=== REPOSITORY: Getting municipal council president by ID: {president_id} ==="
        )

        result = self.supabase_service.get_record_by_id(self.table_name, president_id)

        if not result:
            return None

        return self._map_to_entity(result)

    def get_by_document_id(
        self, document_id: str
    ) -> Optional[MunicipalCouncilPresident]:
        """Get municipal council president by document ID"""
        logger.info(
            f"=== REPOSITORY: Getting municipal council president by document ID: {document_id} ==="
        )

        results = self.supabase_service.get_all_records(
            self.table_name, {"document_id": f"eq.{document_id}"}
        )

        if not results or len(results) == 0:
            return None

        return self._map_to_entity(results[0])

    def update(
        self, president_id: str, president_data: dict
    ) -> MunicipalCouncilPresident:
        """Update a municipal council president"""
        logger.info(
            f"=== REPOSITORY: Updating municipal council president: {president_id} ==="
        )

        update_data = {}

        if "full_name" in president_data:
            update_data["full_name"] = president_data["full_name"]
        if "document_type" in president_data:
            update_data["document_type"] = president_data["document_type"]
        if "document_id" in president_data:
            update_data["document_id"] = president_data["document_id"]
        if "board_position" in president_data:
            update_data["board_position"] = president_data["board_position"]
        if "political_party" in president_data:
            update_data["political_party"] = president_data["political_party"]
        if "election_period" in president_data:
            update_data["election_period"] = president_data["election_period"]
        if "presidency_type" in president_data:
            update_data["presidency_type"] = president_data["presidency_type"]
        if "position_time" in president_data:
            update_data["position_time"] = president_data["position_time"]
        if "institutional_email" in president_data:
            update_data["institutional_email"] = president_data["institutional_email"]
        if "digital_signature" in president_data:
            update_data["digital_signature"] = president_data["digital_signature"]
        if "fingerprint" in president_data:
            update_data["fingerprint"] = president_data["fingerprint"]

        result = self.supabase_service.update_record(
            self.table_name, president_id, update_data
        )

        return self._map_to_entity(result)

    def delete(self, president_id: str) -> bool:
        """Delete a municipal council president"""
        logger.info(
            f"=== REPOSITORY: Deleting municipal council president: {president_id} ==="
        )

        result = self.supabase_service.delete_record(self.table_name, president_id)

        return result
