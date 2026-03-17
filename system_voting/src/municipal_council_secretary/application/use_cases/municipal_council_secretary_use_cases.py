"""
Use Cases - Municipal Council Secretary
Application Layer
SOLID Principles - Single Responsibility, Dependency Inversion
"""

import logging
import re
from typing import List
from system_voting.src.municipal_council_secretary.domain.entities.municipal_council_secretary import (
    MunicipalCouncilSecretary,
    CreateMunicipalCouncilSecretaryDTO,
)
from system_voting.src.municipal_council_secretary.domain.ports.municipal_council_secretary_repository import (
    MunicipalCouncilSecretaryRepositoryPort,
)

logger = logging.getLogger(__name__)


class CreateMunicipalCouncilSecretaryUseCase:
    """Use case for creating a municipal council secretary"""

    def __init__(self, repository: MunicipalCouncilSecretaryRepositoryPort):
        self.repository = repository

    def execute(
        self, data: CreateMunicipalCouncilSecretaryDTO
    ) -> MunicipalCouncilSecretary:
        logger.info(
            f"=== USE CASE: Creating municipal council secretary: {data.full_name} ==="
        )

        if not data.full_name or len(data.full_name.strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")

        valid_document_types = ["CI", "Pasaporte", "Licencia", "Otro"]
        if data.document_type not in valid_document_types:
            raise ValueError(
                f"El tipo de documento debe ser uno de: {', '.join(valid_document_types)}"
            )

        if not data.document_id or len(data.document_id.strip()) < 5:
            raise ValueError(
                "El documento de identidad debe tener al menos 5 caracteres"
            )

        existing = self.repository.get_by_document_id(data.document_id)
        if existing:
            raise ValueError(
                "Ya existe un secretario de consejo municipal con este documento de identidad"
            )

        valid_positions = ["Secretario General", "Secretario de comision"]
        if data.exact_position not in valid_positions:
            raise ValueError(
                f"El cargo exacto debe ser uno de: {', '.join(valid_positions)}"
            )

        if not data.administrative_act or len(data.administrative_act.strip()) < 3:
            raise ValueError("El acto administrativo de eleccion es requerido")

        if not data.possession_date or len(data.possession_date.strip()) < 3:
            raise ValueError("La fecha de posesion es requerida")

        if not data.legal_period or len(data.legal_period.strip()) < 4:
            raise ValueError("El periodo legal debe tener al menos 4 caracteres")

        valid_performance_types = ["ad-hoc", "temporal"]
        if data.performance_type not in valid_performance_types:
            raise ValueError(
                f"La calidad de actuacion debe ser uno de: {', '.join(valid_performance_types)}"
            )

        if not data.institutional_email:
            raise ValueError("El correo institucional es requerido")

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, data.institutional_email):
            raise ValueError("El correo institucional no tiene un formato valido")

        result = self.repository.create(data)
        logger.info(
            f"=== USE CASE: Municipal council secretary created successfully: {result.id} ==="
        )

        return result


class GetAllMunicipalCouncilSecretariesUseCase:
    """Use case for getting all municipal council secretaries"""

    def __init__(self, repository: MunicipalCouncilSecretaryRepositoryPort):
        self.repository = repository

    def execute(self) -> List[MunicipalCouncilSecretary]:
        logger.info("=== USE CASE: Getting all municipal council secretaries ===")
        return self.repository.get_all()


class GetMunicipalCouncilSecretaryByIdUseCase:
    """Use case for getting a municipal council secretary by ID"""

    def __init__(self, repository: MunicipalCouncilSecretaryRepositoryPort):
        self.repository = repository

    def execute(self, secretary_id: str) -> MunicipalCouncilSecretary:
        logger.info(
            f"=== USE CASE: Getting municipal council secretary by ID: {secretary_id} ==="
        )

        if not secretary_id:
            raise ValueError("El ID del secretario de consejo municipal es requerido")

        secretary = self.repository.get_by_id(secretary_id)

        if not secretary:
            raise ValueError("Secretario de consejo municipal no encontrado")

        return secretary


class UpdateMunicipalCouncilSecretaryUseCase:
    """Use case for updating a municipal council secretary"""

    def __init__(self, repository: MunicipalCouncilSecretaryRepositoryPort):
        self.repository = repository

    def execute(self, secretary_id: str, data: dict) -> MunicipalCouncilSecretary:
        logger.info(
            f"=== USE CASE: Updating municipal council secretary: {secretary_id} ==="
        )

        if not secretary_id:
            raise ValueError("El ID del secretario de consejo municipal es requerido")

        if "full_name" in data and len(data["full_name"].strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres")

        if "document_type" in data:
            valid_document_types = ["CI", "Pasaporte", "Licencia", "Otro"]
            if data["document_type"] not in valid_document_types:
                raise ValueError(
                    f"El tipo de documento debe ser uno de: {', '.join(valid_document_types)}"
                )

        if "document_id" in data and len(data["document_id"].strip()) < 5:
            raise ValueError(
                "El documento de identidad debe tener al menos 5 caracteres"
            )

        if "exact_position" in data:
            valid_positions = ["Secretario General", "Secretario de comision"]
            if data["exact_position"] not in valid_positions:
                raise ValueError(
                    f"El cargo exacto debe ser uno de: {', '.join(valid_positions)}"
                )

        if "administrative_act" in data and len(data["administrative_act"].strip()) < 3:
            raise ValueError("El acto administrativo de eleccion es requerido")

        if "possession_date" in data and len(data["possession_date"].strip()) < 3:
            raise ValueError("La fecha de posesion es requerida")

        if "legal_period" in data and len(data["legal_period"].strip()) < 4:
            raise ValueError("El periodo legal debe tener al menos 4 caracteres")

        if "performance_type" in data:
            valid_performance_types = ["ad-hoc", "temporal"]
            if data["performance_type"] not in valid_performance_types:
                raise ValueError(
                    f"La calidad de actuacion debe ser uno de: {', '.join(valid_performance_types)}"
                )

        if "institutional_email" in data:
            email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, data["institutional_email"]):
                raise ValueError("El correo institucional no tiene un formato valido")

        result = self.repository.update(secretary_id, data)
        logger.info(
            f"=== USE CASE: Municipal council secretary updated successfully: {secretary_id} ==="
        )

        return result


class DeleteMunicipalCouncilSecretaryUseCase:
    """Use case for deleting a municipal council secretary"""

    def __init__(self, repository: MunicipalCouncilSecretaryRepositoryPort):
        self.repository = repository

    def execute(self, secretary_id: str) -> bool:
        logger.info(
            f"=== USE CASE: Deleting municipal council secretary: {secretary_id} ==="
        )

        if not secretary_id:
            raise ValueError("El ID del secretario de consejo municipal es requerido")

        result = self.repository.delete(secretary_id)
        logger.info(
            f"=== USE CASE: Municipal council secretary deleted successfully: {secretary_id} ==="
        )

        return result
