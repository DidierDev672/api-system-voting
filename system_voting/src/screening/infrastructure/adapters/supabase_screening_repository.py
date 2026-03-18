"""
Repository Adapter - Screening
Infrastructure Layer - Supabase Implementation
"""

import uuid
import json
import logging
from typing import List, Optional
from supabase_integration import SupabaseService as BaseSupabaseService
from system_voting.src.screening.domain.entities.screening import (
    Screening,
    CreateScreeningDTO,
    ScreeningOption,
    ScreeningQuestion,
)
from system_voting.src.screening.domain.ports.screening_repository import (
    ScreeningRepositoryPort,
)

logger = logging.getLogger(__name__)


class SupabaseScreeningRepository(ScreeningRepositoryPort):
    """Supabase implementation of ScreeningRepositoryPort"""

    def __init__(self):
        self.supabase_service = BaseSupabaseService()
        self.table_name = "screenings"

    def _map_to_entity(self, data: dict) -> Screening:
        """Map database response to Screening entity"""
        questions = []
        if data.get("questions"):
            for q in data["questions"]:
                options = []
                for opt in q.get("optionsAnswer", []):
                    options.append(
                        ScreeningOption(
                            id=opt.get("id", ""),
                            text=opt.get("text", ""),
                            value=opt.get("value", 0),
                        )
                    )
                questions.append(
                    ScreeningQuestion(sound=q.get("sound", ""), optionsAnswer=options)
                )

        return Screening(
            id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            questions=questions,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def create(self, screening_data: CreateScreeningDTO) -> Screening:
        """Create a new screening"""
        logger.info(f"=== REPOSITORY: Creating screening: {screening_data.title} ===")

        screening_id = str(uuid.uuid4())

        # Format questions
        questions_data = []
        for q in screening_data.questions:
            options = []
            for opt in q.get("optionsAnswer", []):
                options.append(
                    {
                        "id": str(uuid.uuid4()),
                        "text": opt.get("text", ""),
                        "value": opt.get("value", 0),
                    }
                )
            questions_data.append(
                {"sound": q.get("sound", ""), "optionsAnswer": options}
            )

        data = {
            "id": screening_id,
            "title": screening_data.title,
            "description": screening_data.description,
            "questions": questions_data,
        }

        result = self.supabase_service.insert_record(self.table_name, data)
        logger.info(f"=== REPOSITORY: Screening created: {result} ===")

        return self._map_to_entity(result)

    def get_all(self) -> List[Screening]:
        """Get all screenings"""
        logger.info("=== REPOSITORY: Getting all screenings ===")

        results = self.supabase_service.get_all_records(self.table_name, {})

        screenings = [self._map_to_entity(r) for r in (results or [])]
        logger.info(f"=== REPOSITORY: Found {len(screenings)} screenings ===")

        return screenings

    def get_by_id(self, screening_id: str) -> Optional[Screening]:
        """Get screening by ID"""
        logger.info(f"=== REPOSITORY: Getting screening by ID: {screening_id} ===")

        result = self.supabase_service.get_record_by_id(self.table_name, screening_id)

        if not result:
            return None

        return self._map_to_entity(result)

    def update(self, screening_id: str, screening_data: dict) -> Screening:
        """Update a screening"""
        logger.info(f"=== REPOSITORY: Updating screening: {screening_id} ===")

        # Format questions if provided
        questions_data = None
        if "questions" in screening_data:
            questions_data = []
            for q in screening_data["questions"]:
                options = []
                for opt in q.get("optionsAnswer", []):
                    options.append(
                        {
                            "id": opt.get("id", str(uuid.uuid4())),
                            "text": opt.get("text", ""),
                            "value": opt.get("value", 0),
                        }
                    )
                questions_data.append(
                    {"sound": q.get("sound", ""), "optionsAnswer": options}
                )

        update_data = {
            "title": screening_data.get("title"),
            "description": screening_data.get("description"),
        }

        if questions_data is not None:
            update_data["questions"] = questions_data

        result = self.supabase_service.update_record(
            self.table_name, screening_id, update_data
        )

        return self._map_to_entity(result)

    def delete(self, screening_id: str) -> bool:
        """Delete a screening"""
        logger.info(f"=== REPOSITORY: Deleting screening: {screening_id} ===")

        result = self.supabase_service.delete_record(self.table_name, screening_id)

        return result
