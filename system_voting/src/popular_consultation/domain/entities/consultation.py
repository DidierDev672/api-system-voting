"""
Entidades de Dominio para Consulta Popular
Arquitectura Hexagonal + Vertical Slicing
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ConsultationStatus(str, Enum):
    """Estados de la consulta popular"""

    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class QuestionType(str, Enum):
    """Tipos de preguntas"""

    TEXT = "text"
    MULTIPLE_CHOICE = "multiple_choice"
    SINGLE_CHOICE = "single_choice"
    SCALE = "scale"


@dataclass
class Question:
    """Pregunta de la consulta popular"""

    id: Optional[str] = None
    text: str = ""
    question_type: QuestionType = QuestionType.TEXT
    options: List[str] = field(default_factory=list)
    required: bool = False

    def __post_init__(self):
        if not self.text or len(self.text.strip()) < 3:
            raise ValueError("El texto de la pregunta debe tener al menos 3 caracteres")

        if self.question_type in [
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.SINGLE_CHOICE,
        ]:
            if not self.options or len(self.options) < 2:
                raise ValueError(
                    "Las preguntas de selección deben tener al menos 2 opciones"
                )


@dataclass
class PopularConsultation:
    """Entidad de Consulta Popular - Dominio Puro"""

    id: Optional[str] = None
    title: str = ""
    description: str = ""
    questions: List[Question] = field(default_factory=list)
    proprietary_representation: str = ""
    status: ConsultationStatus = ConsultationStatus.DRAFT
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if not self.title or len(self.title.strip()) < 5:
            raise ValueError("El título debe tener al menos 5 caracteres")

        if not self.description or len(self.description.strip()) < 10:
            raise ValueError("La descripción debe tener al menos 10 caracteres")

        if not self.proprietary_representation:
            raise ValueError("La representación propietaria es requerida")

        if not self.questions:
            raise ValueError("La consulta debe tener al menos una pregunta")

    def can_be_published(self) -> bool:
        """Verificar si la consulta puede ser publicada"""
        return (
            self.status == ConsultationStatus.DRAFT
            and len(self.questions) > 0
            and all(q.text for q in self.questions)
        )

    def publish(self):
        """Publicar la consulta"""
        if not self.can_be_published():
            raise ValueError("La consulta no puede ser publicada")
        self.status = ConsultationStatus.PUBLISHED

    def close(self):
        """Cerrar la consulta"""
        if self.status != ConsultationStatus.PUBLISHED:
            raise ValueError("Solo las consultas publicadas pueden ser cerradas")
        self.status = ConsultationStatus.CLOSED


@dataclass
class CreateConsultationCommand:
    """Comando para crear una consulta popular"""

    title: str
    description: str
    questions: List[dict]
    proprietary_representation: str
    status: str = "draft"


@dataclass
class UpdateConsultationCommand:
    """Comando para actualizar una consulta popular"""

    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    questions: Optional[List[dict]] = None
    proprietary_representation: Optional[str] = None
    status: Optional[str] = None
