"""
Repository Adapter - Municipal Council Secretary
Infrastructure Layer - Supabase Implementation
"""

import uuid
import logging
from typing import List, Optional
from supabase_integration.services import SupabaseService
from system_voting.src.municipal_council_secretary.domain.entities.municipal_council_secretary import (
    MunicipalCouncilSecretary,
    CreateMunicipalCouncilSecretaryDTO,
)
from system_voting.src.municipal_council_secretary.domain.ports.municipal_council_secretary_repository import (
    MunicipalCouncilSecretaryRepositoryPort,
)

logger = logging.getLogger(__name__)


class SupabaseMunicipalCouncilSecretaryRepository(
    MunicipalCouncilSecretaryRepositoryPort
):
    """Supabase implementation of MunicipalCouncilSecretaryRepositoryPort"""

    def __init__(self):
        self.supabase_service = SupabaseService()
        self.table_name = "municipal_council_secretaries"

    def _map_to_entity(self, data: dict) -> MunicipalCouncilSecretary:
        """Map database response to MunicipalCouncilSecretary entity"""
        return MunicipalCouncilSecretary(
            id=data.get("id", ""),
            full_name=data.get("full_name", ""),
            document_type=data.get("document_type", ""),
            document_id=data.get("document_id", ""),
            exact_position=data.get("exact_position", ""),
            administrative_act=data.get("administrative_act", ""),
            possession_date=data.get("possession_date", ""),
            legal_period=data.get("legal_period", ""),
            professional_title=data.get("professional_title"),
            performance_type=data.get("performance_type", ""),
            institutional_email=data.get("institutional_email", ""),
            digital_signature=data.get("digital_signature"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def create(
        self, secretary_data: CreateMunicipalCouncilSecretaryDTO
    ) -> MunicipalCouncilSecretary:
        """Create a new municipal council secretary"""
        logger.info(
            f"=== REPOSITORY: Creating municipal council secretary: {secretary_data.full_name} ==="
        )

        secretary_id = str(uuid.uuid4())

        data = {
            "id": secretary_id,
            "full_name": secretary_data.full_name,
            "document_type": secretary_data.document_type,
            "document_id": secretary_data.document_id,
            "exact_position": secretary_data.exact_position,
            "administrative_act": secretary_data.administrative_act,
            "possession_date": secretary_data.possession_date,
            "legal_period": secretary_data.legal_period,
            "professional_title": secretary_data.professional_title,
            "performance_type": secretary_data.performance_type,
            "institutional_email": secretary_data.institutional_email,
            "digital_signature": secretary_data.digital_signature,
        }

        result = self.supabase_service.insert_record(self.table_name, data)
        logger.info(
            f"=== REPOSITORY: Municipal council secretary created: {result} ==="
        )

        return self._map_to_entity(result)

    def get_all(self) -> List[MunicipalCouncilSecretary]:
        """Get all municipal council secretaries"""
        logger.info("=== REPOSITORY: Getting all municipal council secretaries ===")

        results = self.supabase_service.get_all_records(self.table_name, {})

        secretaries = [self._map_to_entity(r) for r in (results or [])]
        logger.info(f"=== REPOSITORY: Found {len(secretaries)} secretaries ===")

        return secretaries

    def get_by_id(self, secretary_id: str) -> Optional[MunicipalCouncilSecretary]:
        """Get municipal council secretary by ID"""
        logger.info(
            f"=== REPOSITORY: Getting municipal council secretary by ID: {secretary_id} ==="
        )

        result = self.supabase_service.get_record_by_id(self.table_name, secretary_id)

        if not result:
            return None

        return self._map_to_entity(result)

    def get_by_document_id(
        self, document_id: str
    ) -> Optional[MunicipalCouncilSecretary]:
        """Get municipal council secretary by document ID"""
        logger.info(
            f"=== REPOSITORY: Getting municipal council secretary by document ID: {document_id} ==="
        )

        results = self.supabase_service.get_all_records(
            self.table_name, {"document_id": f"eq.{document_id}"}
        )

        if not results or len(results) == 0:
            return None

        return self._map_to_entity(results[0])

    def update(
        self, secretary_id: str, secretary_data: dict
    ) -> MunicipalCouncilSecretary:
        """Update a municipal council secretary"""
        logger.info(
            f"=== REPOSITORY: Updating municipal council secretary: {secretary_id} ==="
        )

        update_data = {}

        if "full_name" in secretary_data:
            update_data["full_name"] = secretary_data["full_name"]
        if "document_type" in secretary_data:
            update_data["document_type"] = secretary_data["document_type"]
        if "document_id" in secretary_data:
            update_data["document_id"] = secretary_data["document_id"]
        if "exact_position" in secretary_data:
            update_data["exact_position"] = secretary_data["exact_position"]
        if "administrative_act" in secretary_data:
            update_data["administrative_act"] = secretary_data["administrative_act"]
        if "possession_date" in secretary_data:
            update_data["possession_date"] = secretary_data["possession_date"]
        if "legal_period" in secretary_data:
            update_data["legal_period"] = secretary_data["legal_period"]
        if "professional_title" in secretary_data:
            update_data["professional_title"] = secretary_data["professional_title"]
        if "performance_type" in secretary_data:
            update_data["performance_type"] = secretary_data["performance_type"]
        if "institutional_email" in secretary_data:
            update_data["institutional_email"] = secretary_data["institutional_email"]
        if "digital_signature" in secretary_data:
            update_data["digital_signature"] = secretary_data["digital_signature"]

        result = self.supabase_service.update_record(
            self.table_name, secretary_id, update_data
        )

        return self._map_to_entity(result)

    def delete(self, secretary_id: str) -> bool:
        """Delete a municipal council secretary"""
        logger.info(
            f"=== REPOSITORY: Deleting municipal council secretary: {secretary_id} ==="
        )

        result = self.supabase_service.delete_record(self.table_name, secretary_id)

        return result
