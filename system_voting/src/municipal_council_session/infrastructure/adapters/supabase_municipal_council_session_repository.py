"""
Repository Adapter - Municipal Council Session
Infrastructure Layer - Supabase Implementation
"""

import uuid
import logging
from typing import List, Optional
from supabase_integration.services import SupabaseService
from system_voting.src.municipal_council_session.domain.entities.municipal_council_session import (
    MunicipalCouncilSession,
    CreateMunicipalCouncilSessionDTO,
)
from system_voting.src.municipal_council_session.domain.ports.municipal_council_session_repository import (
    MunicipalCouncilSessionRepositoryPort,
)

logger = logging.getLogger(__name__)


class SupabaseMunicipalCouncilSessionRepository(MunicipalCouncilSessionRepositoryPort):
    """Supabase implementation of MunicipalCouncilSessionRepositoryPort"""

    def __init__(self):
        self.supabase_service = SupabaseService()
        self.table_name = "municipal_council_sessions"

    def _map_to_entity(self, data: dict) -> MunicipalCouncilSession:
        """Map database response to MunicipalCouncilSession entity"""
        return MunicipalCouncilSession(
            id=data.get("id", ""),
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
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def create(
        self, session_data: CreateMunicipalCouncilSessionDTO
    ) -> MunicipalCouncilSession:
        """Create a new municipal council session"""
        logger.info(
            f"=== REPOSITORY: Creating municipal council session: {session_data.title_session} ==="
        )

        session_id = str(uuid.uuid4())

        data = {
            "id": session_id,
            "title_session": session_data.title_session,
            "type_session": session_data.type_session,
            "status_session": session_data.status_session,
            "date_hour_start": session_data.date_hour_start,
            "date_hour_end": session_data.date_hour_end,
            "modality": session_data.modality,
            "place_enclosure": session_data.place_enclosure,
            "orden_day": session_data.orden_day,
            "quorum_required": session_data.quorum_required,
            "id_president": session_data.id_president,
            "id_secretary": session_data.id_secretary,
        }

        result = self.supabase_service.insert_record(self.table_name, data)
        logger.info(f"=== REPOSITORY: Municipal council session created: {result} ===")

        return self._map_to_entity(result)

    def get_all(self) -> List[MunicipalCouncilSession]:
        """Get all municipal council sessions"""
        logger.info("=== REPOSITORY: Getting all municipal council sessions ===")

        results = self.supabase_service.get_all_records(self.table_name, {})

        sessions = [self._map_to_entity(r) for r in (results or [])]
        logger.info(f"=== REPOSITORY: Found {len(sessions)} sessions ===")

        return sessions

    def get_by_id(self, session_id: str) -> Optional[MunicipalCouncilSession]:
        """Get municipal council session by ID"""
        logger.info(
            f"=== REPOSITORY: Getting municipal council session by ID: {session_id} ==="
        )

        result = self.supabase_service.get_record_by_id(self.table_name, session_id)

        if not result:
            return None

        return self._map_to_entity(result)

    def update(self, session_id: str, session_data: dict) -> MunicipalCouncilSession:
        """Update a municipal council session"""
        logger.info(
            f"=== REPOSITORY: Updating municipal council session: {session_id} ==="
        )

        update_data = {}

        if "title_session" in session_data:
            update_data["title_session"] = session_data["title_session"]
        if "type_session" in session_data:
            update_data["type_session"] = session_data["type_session"]
        if "status_session" in session_data:
            update_data["status_session"] = session_data["status_session"]
        if "date_hour_start" in session_data:
            update_data["date_hour_start"] = session_data["date_hour_start"]
        if "date_hour_end" in session_data:
            update_data["date_hour_end"] = session_data["date_hour_end"]
        if "modality" in session_data:
            update_data["modality"] = session_data["modality"]
        if "place_enclosure" in session_data:
            update_data["place_enclosure"] = session_data["place_enclosure"]
        if "orden_day" in session_data:
            update_data["orden_day"] = session_data["orden_day"]
        if "quorum_required" in session_data:
            update_data["quorum_required"] = session_data["quorum_required"]
        if "id_president" in session_data:
            update_data["id_president"] = session_data["id_president"]
        if "id_secretary" in session_data:
            update_data["id_secretary"] = session_data["id_secretary"]

        result = self.supabase_service.update_record(
            self.table_name, session_id, update_data
        )

        return self._map_to_entity(result)

    def delete(self, session_id: str) -> bool:
        """Delete a municipal council session"""
        logger.info(
            f"=== REPOSITORY: Deleting municipal council session: {session_id} ==="
        )

        result = self.supabase_service.delete_record(self.table_name, session_id)

        return result
