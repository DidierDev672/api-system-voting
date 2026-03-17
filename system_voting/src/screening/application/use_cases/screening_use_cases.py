"""
Use Cases - Screening
Application Layer
SOLID Principles - Single Responsibility, Dependency Inversion
"""

import logging
from typing import List
from system_voting.src.screening.domain.entities.screening import (
    Screening,
    CreateScreeningDTO,
)
from system_voting.src.screening.domain.ports.screening_repository import (
    ScreeningRepositoryPort,
)

logger = logging.getLogger(__name__)


class CreateScreeningUseCase:
    """Use case for creating a screening"""

    def __init__(self, repository: ScreeningRepositoryPort):
        self.repository = repository

    def execute(self, data: CreateScreeningDTO) -> Screening:
        logger.info(f"=== USE CASE: Creating screening: {data.title} ===")

        # Validation
        if not data.title or len(data.title.strip()) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres")

        if not data.description or len(data.description.strip()) == 0:
            raise ValueError("La descripción es requerida")

        if not data.questions or len(data.questions) == 0:
            raise ValueError("Debe agregar al menos una pregunta")

        # Validate each question
        for i, q in enumerate(data.questions):
            if not q.get("sound"):
                raise ValueError(f"La pregunta {i + 1} debe tener un sonido")

            options = q.get("optionsAnswer", [])
            if len(options) < 2:
                raise ValueError(f"La pregunta {i + 1} debe tener al menos 2 opciones")

            has_correct = any(opt.get("value", 0) == 1 for opt in options)
            if not has_correct:
                raise ValueError(f"La pregunta {i + 1} debe tener una opción correcta")

        result = self.repository.create(data)
        logger.info(f"=== USE CASE: Screening created successfully: {result.id} ===")

        return result


class GetAllScreeningsUseCase:
    """Use case for getting all screenings"""

    def __init__(self, repository: ScreeningRepositoryPort):
        self.repository = repository

    def execute(self) -> List[Screening]:
        logger.info("=== USE CASE: Getting all screenings ===")
        return self.repository.get_all()


class GetScreeningByIdUseCase:
    """Use case for getting a screening by ID"""

    def __init__(self, repository: ScreeningRepositoryPort):
        self.repository = repository

    def execute(self, screening_id: str) -> Screening:
        logger.info(f"=== USE CASE: Getting screening by ID: {screening_id} ===")

        if not screening_id:
            raise ValueError("El ID del tamizaje es requerido")

        screening = self.repository.get_by_id(screening_id)

        if not screening:
            raise ValueError("Tamizaje no encontrado")

        return screening


class UpdateScreeningUseCase:
    """Use case for updating a screening"""

    def __init__(self, repository: ScreeningRepositoryPort):
        self.repository = repository

    def execute(self, screening_id: str, data: dict) -> Screening:
        logger.info(f"=== USE CASE: Updating screening: {screening_id} ===")

        if not screening_id:
            raise ValueError("El ID del tamizaje es requerido")

        # Validation
        if "title" in data and len(data["title"].strip()) < 3:
            raise ValueError("El título debe tener al menos 3 caracteres")

        if "description" in data and len(data["description"].strip()) == 0:
            raise ValueError("La descripción es requerida")

        result = self.repository.update(screening_id, data)
        logger.info(f"=== USE CASE: Screening updated successfully: {screening_id} ===")

        return result


class DeleteScreeningUseCase:
    """Use case for deleting a screening"""

    def __init__(self, repository: ScreeningRepositoryPort):
        self.repository = repository

    def execute(self, screening_id: str) -> bool:
        logger.info(f"=== USE CASE: Deleting screening: {screening_id} ===")

        if not screening_id:
            raise ValueError("El ID del tamizaje es requerido")

        result = self.repository.delete(screening_id)
        logger.info(f"=== USE CASE: Screening deleted successfully: {screening_id} ===")

        return result
