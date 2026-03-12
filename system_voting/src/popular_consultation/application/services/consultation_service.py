"""
Servicio de Aplicación para Consulta Popular
Capa de aplicación - Coordina el flujo de datos entre capas
"""

from typing import List, Optional
import logging
from system_voting.src.popular_consultation.domain.entities.consultation import (
    PopularConsultation,
    Question,
    QuestionType,
    ConsultationStatus,
    CreateConsultationCommand,
    UpdateConsultationCommand,
)
from system_voting.src.popular_consultation.infrastructure.repositories.supabase_consultation_repository import (
    SupabaseConsultationRepository,
)

logger = logging.getLogger(__name__)


class ConsultationService:
    """Servicio de aplicación para consultas populares"""

    def __init__(self, repository=None):
        self.repository = repository or SupabaseConsultationRepository()

    def create_consultation(
        self, command: CreateConsultationCommand
    ) -> PopularConsultation:
        """Crear una nueva consulta popular"""
        logger.info(f"=== SERVICIO: Creando consulta: {command.title} ===")

        questions = []
        for q_data in command.questions:
            question_type = q_data.get("question_type", "text")
            if isinstance(question_type, str):
                try:
                    question_type = QuestionType(question_type)
                except ValueError:
                    question_type = QuestionType.TEXT

            questions.append(
                Question(
                    id=q_data.get("id"),
                    text=q_data.get("text", ""),
                    question_type=question_type,
                    options=q_data.get("options", []),
                    required=q_data.get("required", False),
                )
            )

        try:
            status = (
                ConsultationStatus(command.status)
                if command.status
                else ConsultationStatus.DRAFT
            )
        except ValueError:
            status = ConsultationStatus.DRAFT

        consultation = PopularConsultation(
            title=command.title,
            description=command.description,
            questions=questions,
            proprietary_representation=command.proprietary_representation,
            status=status,
        )

        result = self.repository.save(consultation)
        logger.info(f"=== SERVICIO: Consulta creada exitosamente: {result.id} ===")
        return result

    def get_consultation(self, consultation_id: str) -> Optional[PopularConsultation]:
        """Obtener una consulta por ID"""
        logger.info(f"=== SERVICIO: Obteniendo consulta: {consultation_id} ===")
        return self.repository.get_by_id(consultation_id)

    def get_all_consultations(self) -> List[PopularConsultation]:
        """Obtener todas las consultas"""
        logger.info("=== SERVICIO: Obteniendo todas las consultas ===")
        return self.repository.get_all()

    def update_consultation(
        self, command: UpdateConsultationCommand
    ) -> PopularConsultation:
        """Actualizar una consulta"""
        logger.info(f"=== SERVICIO: Actualizando consulta: {command.id} ===")

        existing = self.repository.get_by_id(command.id)
        if not existing:
            raise ValueError(f"Consulta no encontrada: {command.id}")

        if command.title is not None:
            existing.title = command.title
        if command.description is not None:
            existing.description = command.description
        if command.proprietary_representation is not None:
            existing.proprietary_representation = command.proprietary_representation
        if command.status is not None:
            try:
                existing.status = ConsultationStatus(command.status)
            except ValueError:
                pass

        if command.questions is not None:
            questions = []
            for q_data in command.questions:
                question_type = q_data.get("question_type", "text")
                if isinstance(question_type, str):
                    try:
                        question_type = QuestionType(question_type)
                    except ValueError:
                        question_type = QuestionType.TEXT

                questions.append(
                    Question(
                        id=q_data.get("id"),
                        text=q_data.get("text", ""),
                        question_type=question_type,
                        options=q_data.get("options", []),
                        required=q_data.get("required", False),
                    )
                )
            existing.questions = questions

        result = self.repository.update(existing)
        logger.info(f"=== SERVICIO: Consulta actualizada: {result.id} ===")
        return result

    def delete_consultation(self, consultation_id: str) -> bool:
        """Eliminar una consulta"""
        logger.info(f"=== SERVICIO: Eliminando consulta: {consultation_id} ===")
        return self.repository.delete(consultation_id)

    def publish_consultation(self, consultation_id: str) -> PopularConsultation:
        """Publicar una consulta"""
        logger.info(f"=== SERVICIO: Publicando consulta: {consultation_id} ===")

        consultation = self.repository.get_by_id(consultation_id)
        if not consultation:
            raise ValueError(f"Consulta no encontrada: {consultation_id}")

        consultation.publish()
        result = self.repository.update(consultation)
        logger.info(f"=== SERVICIO: Consulta publicada: {result.id} ===")
        return result

    def close_consultation(self, consultation_id: str) -> PopularConsultation:
        """Cerrar una consulta"""
        logger.info(f"=== SERVICIO: Cerrando consulta: {consultation_id} ===")

        consultation = self.repository.get_by_id(consultation_id)
        if not consultation:
            raise ValueError(f"Consulta no encontrada: {consultation_id}")

        consultation.close()
        result = self.repository.update(consultation)
        logger.info(f"=== SERVICIO: Consulta cerrada: {result.id} ===")
        return result
