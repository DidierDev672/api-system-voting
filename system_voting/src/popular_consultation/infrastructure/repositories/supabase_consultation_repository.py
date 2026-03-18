"""
Repositorio Concreto para Consulta Popular usando Supabase
Adapter que implementa el puerto del repositorio
"""

from typing import List, Optional, Dict, Any
import logging
from supabase_integration import consultations_service as consultations_svc
from system_voting.src.popular_consultation.domain.entities.consultation import (
    PopularConsultation,
    Question,
    QuestionType,
    ConsultationStatus,
)

logger = logging.getLogger(__name__)


class SupabaseConsultationRepository:
    """Implementación del repositorio con Supabase"""

    def __init__(self):
        self.supabase_service = consultations_svc

    def save(self, consultation: PopularConsultation) -> PopularConsultation:
        """Crear una nueva consulta popular en Supabase"""
        logger.info(f"=== INICIO SAVE CONSULTATION: {consultation.title} ===")

        consultation_data = {
            "title": consultation.title,
            "description": consultation.description,
            "questions": self._serialize_questions(consultation.questions),
            "proprietary_representation": consultation.proprietary_representation,
            "status": consultation.status.value,
        }

        result = self.supabase_service.create_consultation(consultation_data)
        logger.info(f"Consulta guardada: {result}")

        return self._map_to_entity(result)

    def get_by_id(self, consultation_id: str) -> Optional[PopularConsultation]:
        """Obtener consulta por ID desde Supabase"""
        logger.info(f"=== INICIO GET BY ID: {consultation_id} ===")

        if not consultation_id:
            logger.warning("ID de consulta no proporcionado")
            return None

        result = self.supabase_service.get_consultation_by_id(consultation_id)

        if not result:
            logger.warning(f"Consulta no encontrada: {consultation_id}")
            return None

        return self._map_to_entity(result)

    def get_all(self) -> List[PopularConsultation]:
        """Obtener todas las consultas desde Supabase"""
        logger.info("=== INICIO GET ALL CONSULTATIONS ===")

        results = self.supabase_service.get_all_consultations()
        logger.info(f"Consultas obtenidas: {len(results) if results else 0}")

        return [self._map_to_entity(r) for r in results] if results else []

    def update(self, consultation: PopularConsultation) -> PopularConsultation:
        """Actualizar consulta en Supabase"""
        logger.info(f"=== INICIO UPDATE CONSULTATION: {consultation.id} ===")

        consultation_data = {
            "title": consultation.title,
            "description": consultation.description,
            "questions": self._serialize_questions(consultation.questions),
            "proprietary_representation": consultation.proprietary_representation,
            "status": consultation.status.value,
        }

        result = self.supabase_service.update_consultation(
            consultation.id, consultation_data
        )
        logger.info(f"Consulta actualizada: {result}")

        return self._map_to_entity(result)

    def delete(self, consultation_id: str) -> bool:
        """Eliminar consulta de Supabase"""
        logger.info(f"=== INICIO DELETE CONSULTATION: {consultation_id} ===")

        result = self.supabase_service.delete_consultation(consultation_id)
        logger.info(f"Resultado eliminación: {result}")

        return result

    def _serialize_questions(self, questions: List[Question]) -> List[Dict[str, Any]]:
        """Serializar preguntas para Supabase"""
        return [
            {
                "id": q.id or "",
                "text": q.text,
                "question_type": q.question_type.value
                if isinstance(q.question_type, QuestionType)
                else q.question_type,
                "options": q.options,
                "required": q.required,
            }
            for q in questions
        ]

    def _map_to_entity(self, data: Dict[str, Any]) -> PopularConsultation:
        """Mapear datos de Supabase a entidad de dominio"""
        questions = []
        if data.get("questions"):
            for q in data["questions"]:
                question_type = q.get("question_type", "text")
                if isinstance(question_type, str):
                    try:
                        question_type = QuestionType(question_type)
                    except ValueError:
                        question_type = QuestionType.TEXT

                questions.append(
                    Question(
                        id=q.get("id"),
                        text=q.get("text", ""),
                        question_type=question_type,
                        options=q.get("options", []),
                        required=q.get("required", False),
                    )
                )

        status = data.get("status", "draft")
        if isinstance(status, str):
            try:
                status = ConsultationStatus(status)
            except ValueError:
                status = ConsultationStatus.DRAFT

        return PopularConsultation(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            questions=questions,
            proprietary_representation=data.get("proprietary_representation", ""),
            status=status,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
