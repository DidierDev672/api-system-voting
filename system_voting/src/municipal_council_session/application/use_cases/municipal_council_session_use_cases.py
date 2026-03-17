"""
Use Cases - Municipal Council Session
Application Layer
SOLID Principles - Single Responsibility, Dependency Inversion
"""

import logging
from typing import List
from system_voting.src.municipal_council_session.domain.entities.municipal_council_session import (
    MunicipalCouncilSession,
    CreateMunicipalCouncilSessionDTO,
)
from system_voting.src.municipal_council_session.domain.ports.municipal_council_session_repository import (
    MunicipalCouncilSessionRepositoryPort,
)

logger = logging.getLogger(__name__)


class CreateMunicipalCouncilSessionUseCase:
    """Use case for creating a municipal council session"""

    def __init__(self, repository: MunicipalCouncilSessionRepositoryPort):
        self.repository = repository

    def execute(
        self, data: CreateMunicipalCouncilSessionDTO
    ) -> MunicipalCouncilSession:
        logger.info(
            f"=== USE CASE: Creating municipal council session: {data.title_session} ==="
        )

        if not data.title_session or len(data.title_session.strip()) < 3:
            raise ValueError("El titulo de la sesion debe tener al menos 3 caracteres")

        valid_types = ["Ordinaria", "Extraordinaria", "Especial", "Instalacion"]
        if data.type_session not in valid_types:
            raise ValueError(
                f"El tipo de sesion debe ser uno de: {', '.join(valid_types)}"
            )

        valid_status = [
            "Convocada",
            "En progreso",
            "Realizada",
            "Cancelada",
            "Postergada",
        ]
        if data.status_session not in valid_status:
            raise ValueError(
                f"El estado de la sesion debe ser uno de: {', '.join(valid_status)}"
            )

        if not data.date_hour_start:
            raise ValueError("La fecha y hora de inicio es requerida")

        if not data.date_hour_end:
            raise ValueError("La fecha y hora de fin es requerida")

        valid_modalities = ["presencial", "virtual", "hibrida"]
        if data.modality not in valid_modalities:
            raise ValueError(
                f"La modalidad debe ser una de: {', '.join(valid_modalities)}"
            )

        if not data.place_enclosure or len(data.place_enclosure.strip()) < 3:
            raise ValueError("El lugar de enclosure es requerido")

        if not data.orden_day or len(data.orden_day.strip()) < 3:
            raise ValueError("El orden del dia es requerido")

        if not data.quorum_required or data.quorum_required < 1:
            raise ValueError("El quorum requerido debe ser al menos 1")

        if not data.id_president:
            raise ValueError("El ID del presidente es requerido")

        if not data.id_secretary:
            raise ValueError("El ID del secretario es requerido")

        result = self.repository.create(data)
        logger.info(
            f"=== USE CASE: Municipal council session created successfully: {result.id} ==="
        )

        return result


class GetAllMunicipalCouncilSessionsUseCase:
    """Use case for getting all municipal council sessions"""

    def __init__(self, repository: MunicipalCouncilSessionRepositoryPort):
        self.repository = repository

    def execute(self) -> List[MunicipalCouncilSession]:
        logger.info("=== USE CASE: Getting all municipal council sessions ===")
        return self.repository.get_all()


class GetMunicipalCouncilSessionByIdUseCase:
    """Use case for getting a municipal council session by ID"""

    def __init__(self, repository: MunicipalCouncilSessionRepositoryPort):
        self.repository = repository

    def execute(self, session_id: str) -> MunicipalCouncilSession:
        logger.info(
            f"=== USE CASE: Getting municipal council session by ID: {session_id} ==="
        )

        if not session_id:
            raise ValueError("El ID de la sesion es requerido")

        session = self.repository.get_by_id(session_id)

        if not session:
            raise ValueError("Sesion de consejo municipal no encontrada")

        return session


class UpdateMunicipalCouncilSessionUseCase:
    """Use case for updating a municipal council session"""

    def __init__(self, repository: MunicipalCouncilSessionRepositoryPort):
        self.repository = repository

    def execute(self, session_id: str, data: dict) -> MunicipalCouncilSession:
        logger.info(
            f"=== USE CASE: Updating municipal council session: {session_id} ==="
        )

        if not session_id:
            raise ValueError("El ID de la sesion es requerido")

        if "title_session" in data and len(data["title_session"].strip()) < 3:
            raise ValueError("El titulo de la sesion debe tener al menos 3 caracteres")

        if "type_session" in data:
            valid_types = ["Ordinaria", "Extraordinaria", "Especial", "Instalacion"]
            if data["type_session"] not in valid_types:
                raise ValueError(
                    f"El tipo de sesion debe ser uno de: {', '.join(valid_types)}"
                )

        if "status_session" in data:
            valid_status = [
                "Convocada",
                "En progreso",
                "Realizada",
                "Cancelada",
                "Postergada",
            ]
            if data["status_session"] not in valid_status:
                raise ValueError(
                    f"El estado de la sesion debe ser uno de: {', '.join(valid_status)}"
                )

        if "modality" in data:
            valid_modalities = ["presencial", "virtual", "hibrida"]
            if data["modality"] not in valid_modalities:
                raise ValueError(
                    f"La modalidad debe ser una de: {', '.join(valid_modalities)}"
                )

        if "quorum_required" in data and data["quorum_required"] < 1:
            raise ValueError("El quorum requerido debe ser al menos 1")

        result = self.repository.update(session_id, data)
        logger.info(
            f"=== USE CASE: Municipal council session updated successfully: {session_id} ==="
        )

        return result


class DeleteMunicipalCouncilSessionUseCase:
    """Use case for deleting a municipal council session"""

    def __init__(self, repository: MunicipalCouncilSessionRepositoryPort):
        self.repository = repository

    def execute(self, session_id: str) -> bool:
        logger.info(
            f"=== USE CASE: Deleting municipal council session: {session_id} ==="
        )

        if not session_id:
            raise ValueError("El ID de la sesion es requerido")

        result = self.repository.delete(session_id)
        logger.info(
            f"=== USE CASE: Municipal council session deleted successfully: {session_id} ==="
        )

        return result
