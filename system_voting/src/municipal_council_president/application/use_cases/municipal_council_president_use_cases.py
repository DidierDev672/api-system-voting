"""
Use Cases - Municipal Council President
Application Layer
SOLID Principles - Single Responsibility, Dependency Inversion
"""

import logging
import re
from typing import List
from system_voting.src.municipal_council_president.domain.entities.municipal_council_president import (
    MunicipalCouncilPresident,
    CreateMunicipalCouncilPresidentDTO,
)
from system_voting.src.municipal_council_president.domain.ports.municipal_council_president_repository import (
    MunicipalCouncilPresidentRepositoryPort,
)

logger = logging.getLogger(__name__)


class CreateMunicipalCouncilPresidentUseCase:
    """Use case for creating a municipal council president"""

    def __init__(self, repository: MunicipalCouncilPresidentRepositoryPort):
        self.repository = repository

    def execute(
        self, data: CreateMunicipalCouncilPresidentDTO
    ) -> MunicipalCouncilPresident:
        logger.info(
            f"=== USE CASE: Creating municipal council president: {data.full_name} ==="
        )

        # Validate full name
        if not data.full_name or len(data.full_name.strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")

        # Validate document type
        valid_document_types = ["CI", "Pasaporte", "Licencia", "Otro"]
        if data.document_type not in valid_document_types:
            raise ValueError(
                f"El tipo de documento debe ser uno de: {', '.join(valid_document_types)}"
            )

        # Validate document ID
        if not data.document_id or len(data.document_id.strip()) < 5:
            raise ValueError(
                "El documento de identidad debe tener al menos 5 caracteres"
            )

        # Check for duplicate document ID
        existing = self.repository.get_by_document_id(data.document_id)
        if existing:
            raise ValueError(
                "Ya existe un presidente de consejo municipal con este documento de identidad"
            )

        # Validate board position
        if not data.board_position or len(data.board_position.strip()) < 3:
            raise ValueError("El cargo de la mesa debe tener al menos 3 caracteres")

        # Validate political party
        if not data.political_party or len(data.political_party.strip()) < 2:
            raise ValueError("El partido politico debe tener al menos 2 caracteres")

        # Validate election period
        if not data.election_period or len(data.election_period.strip()) < 4:
            raise ValueError("El periodo de eleccion debe tener al menos 4 caracteres")

        # Validate presidency type
        valid_presidency_types = ["Propietario", "Suplente", "Interino"]
        if data.presidency_type not in valid_presidency_types:
            raise ValueError(
                f"La calidad de presidencia debe ser uno de: {', '.join(valid_presidency_types)}"
            )

        # Validate position time
        if not data.position_time or len(data.position_time.strip()) < 3:
            raise ValueError(
                "La hora de toma de posicion debe tener al menos 3 caracteres"
            )

        # Validate institutional email
        if not data.institutional_email:
            raise ValueError("El correo institucional es requerido")

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, data.institutional_email):
            raise ValueError("El correo institucional no tiene un formato valido")

        result = self.repository.create(data)
        logger.info(
            f"=== USE CASE: Municipal council president created successfully: {result.id} ==="
        )

        return result


class GetAllMunicipalCouncilPresidentsUseCase:
    """Use case for getting all municipal council presidents"""

    def __init__(self, repository: MunicipalCouncilPresidentRepositoryPort):
        self.repository = repository

    def execute(self) -> List[MunicipalCouncilPresident]:
        logger.info("=== USE CASE: Getting all municipal council presidents ===")
        return self.repository.get_all()


class GetMunicipalCouncilPresidentByIdUseCase:
    """Use case for getting a municipal council president by ID"""

    def __init__(self, repository: MunicipalCouncilPresidentRepositoryPort):
        self.repository = repository

    def execute(self, president_id: str) -> MunicipalCouncilPresident:
        logger.info(
            f"=== USE CASE: Getting municipal council president by ID: {president_id} ==="
        )

        if not president_id:
            raise ValueError("El ID del presidente de consejo municipal es requerido")

        president = self.repository.get_by_id(president_id)

        if not president:
            raise ValueError("Presidente de consejo municipal no encontrado")

        return president


class UpdateMunicipalCouncilPresidentUseCase:
    """Use case for updating a municipal council president"""

    def __init__(self, repository: MunicipalCouncilPresidentRepositoryPort):
        self.repository = repository

    def execute(self, president_id: str, data: dict) -> MunicipalCouncilPresident:
        logger.info(
            f"=== USE CASE: Updating municipal council president: {president_id} ==="
        )

        if not president_id:
            raise ValueError("El ID del presidente de consejo municipal es requerido")

        # Validate full name if provided
        if "full_name" in data and len(data["full_name"].strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")

        # Validate document type if provided
        if "document_type" in data:
            valid_document_types = ["CI", "Pasaporte", "Licencia", "Otro"]
            if data["document_type"] not in valid_document_types:
                raise ValueError(
                    f"El tipo de documento debe ser uno de: {', '.join(valid_document_types)}"
                )

        # Validate document ID if provided
        if "document_id" in data and len(data["document_id"].strip()) < 5:
            raise ValueError(
                "El documento de identidad debe tener al menos 5 caracteres"
            )

        # Validate board position if provided
        if "board_position" in data and len(data["board_position"].strip()) < 3:
            raise ValueError("El cargo de la mesa debe tener al menos 3 caracteres")

        # Validate political party if provided
        if "political_party" in data and len(data["political_party"].strip()) < 2:
            raise ValueError("El partido politico debe tener al menos 2 caracteres")

        # Validate election period if provided
        if "election_period" in data and len(data["election_period"].strip()) < 4:
            raise ValueError("El periodo de eleccion debe tener al menos 4 caracteres")

        # Validate presidency type if provided
        if "presidency_type" in data:
            valid_presidency_types = ["Propietario", "Suplente", "Interino"]
            if data["presidency_type"] not in valid_presidency_types:
                raise ValueError(
                    f"La calidad de presidencia debe ser uno de: {', '.join(valid_presidency_types)}"
                )

        # Validate position time if provided
        if "position_time" in data and len(data["position_time"].strip()) < 3:
            raise ValueError(
                "La hora de toma de posicion debe tener al menos 3 caracteres"
            )

        # Validate institutional email if provided
        if "institutional_email" in data:
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, data["institutional_email"]):
                raise ValueError("El correo institucional no tiene un formato valido")

        result = self.repository.update(president_id, data)
        logger.info(
            f"=== USE CASE: Municipal council president updated successfully: {president_id} ==="
        )

        return result


class DeleteMunicipalCouncilPresidentUseCase:
    """Use case for deleting a municipal council president"""

    def __init__(self, repository: MunicipalCouncilPresidentRepositoryPort):
        self.repository = repository

    def execute(self, president_id: str) -> bool:
        logger.info(
            f"=== USE CASE: Deleting municipal council president: {president_id} ==="
        )

        if not president_id:
            raise ValueError("El ID del presidente de consejo municipal es requerido")

        result = self.repository.delete(president_id)
        logger.info(
            f"=== USE CASE: Municipal council president deleted successfully: {president_id} ==="
        )

        return result
