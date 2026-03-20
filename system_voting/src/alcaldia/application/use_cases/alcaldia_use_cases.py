"""
Use Cases - Alcaldia
Application Layer
SOLID Principles - Single Responsibility
"""

import logging
import re
from typing import List
from system_voting.src.alcaldia.domain.entities.alcaldia import (
    Alcaldia,
    CreateAlcaldiaDTO,
    UpdateAlcaldiaDTO,
)
from system_voting.src.alcaldia.domain.ports.alcaldia_repository import (
    AlcaldiaRepositoryPort,
)

logger = logging.getLogger(__name__)


class CreateAlcaldiaUseCase:
    """Use case for creating a new alcaldia"""

    def __init__(self, repository: AlcaldiaRepositoryPort):
        self.repository = repository

    def execute(self, data: CreateAlcaldiaDTO) -> Alcaldia:
        logger.info(f"=== USE CASE: Creating alcaldia: {data.nombre_entidad} ===")

        if not data.nombre_entidad or len(data.nombre_entidad.strip()) < 3:
            raise ValueError("El nombre de la entidad debe tener al menos 3 caracteres")

        if not data.nit or not self._validate_nit(data.nit):
            raise ValueError("El NIT es inválido (debe tener formato XX-XXXXXXX-X)")

        if not data.codigo_sigep or len(data.codigo_sigep.strip()) < 1:
            raise ValueError("El código SIGEP es requerido")

        if data.orden_entidad not in ["Municipal", "Distrital"]:
            raise ValueError("La orden de entidad debe ser 'Municipal' o 'Distrital'")

        if not data.municipio or len(data.municipio.strip()) < 2:
            raise ValueError("El municipio es requerido")

        if not data.direccion_fisica or len(data.direccion_fisica.strip()) < 5:
            raise ValueError("La dirección física es requerida")

        if not data.dominio or len(data.dominio.strip()) < 3:
            raise ValueError("El dominio es requerido")

        if not data.correo_institucional or not self._validate_email(
            data.correo_institucional
        ):
            raise ValueError("El correo institucional es inválido")

        if not data.id_alcalde:
            raise ValueError("El ID del alcalde es requerido")

        if not data.nombre_alcalde or len(data.nombre_alcalde.strip()) < 3:
            raise ValueError("El nombre del alcalde es requerido")

        if not data.acto_posesion or len(data.acto_posesion.strip()) < 1:
            raise ValueError("El acto de posesión es requerido")

        result = self.repository.create(data)
        logger.info(f"=== USE CASE: Alcaldia created: {result.id} ===")

        return result

    def _validate_nit(self, nit: str) -> bool:
        """Validate NIT format XX-XXXXXXX-X"""
        pattern = r"^\d{2}-\d{7,8}-\d$"
        return bool(re.match(pattern, nit))

    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))


class GetAllAlcaldiasUseCase:
    """Use case for getting all alcaldias"""

    def __init__(self, repository: AlcaldiaRepositoryPort):
        self.repository = repository

    def execute(self) -> List[Alcaldia]:
        logger.info("=== USE CASE: Getting all alcaldias ===")
        return self.repository.get_all()


class GetAlcaldiaByIdUseCase:
    """Use case for getting alcaldia by ID"""

    def __init__(self, repository: AlcaldiaRepositoryPort):
        self.repository = repository

    def execute(self, alcaldia_id: str) -> Alcaldia:
        logger.info(f"=== USE CASE: Getting alcaldia by ID: {alcaldia_id} ===")

        if not alcaldia_id:
            raise ValueError("El ID de la alcaldía es requerido")

        alcaldia = self.repository.get_by_id(alcaldia_id)

        if not alcaldia:
            raise ValueError("Alcaldía no encontrada")

        return alcaldia


class UpdateAlcaldiaUseCase:
    """Use case for updating an alcaldia"""

    def __init__(self, repository: AlcaldiaRepositoryPort):
        self.repository = repository

    def execute(self, alcaldia_id: str, data: UpdateAlcaldiaDTO) -> Alcaldia:
        logger.info(f"=== USE CASE: Updating alcaldia: {alcaldia_id} ===")

        if not alcaldia_id:
            raise ValueError("El ID de la alcaldía es requerido")

        if data.orden_entidad and data.orden_entidad not in ["Municipal", "Distrital"]:
            raise ValueError("La orden de entidad debe ser 'Municipal' o 'Distrital'")

        if data.nit:
            pattern = r"^\d{2}-\d{7,8}-\d$"
            if not re.match(pattern, data.nit):
                raise ValueError("El NIT es inválido (debe tener formato XX-XXXXXXX-X)")

        if data.correo_institucional:
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(pattern, data.correo_institucional):
                raise ValueError("El correo institucional es inválido")

        result = self.repository.update(alcaldia_id, data)
        logger.info(f"=== USE CASE: Alcaldia updated: {alcaldia_id} ===")

        return result


class DeleteAlcaldiaUseCase:
    """Use case for deleting an alcaldia"""

    def __init__(self, repository: AlcaldiaRepositoryPort):
        self.repository = repository

    def execute(self, alcaldia_id: str) -> bool:
        logger.info(f"=== USE CASE: Deleting alcaldia: {alcaldia_id} ===")

        if not alcaldia_id:
            raise ValueError("El ID de la alcaldía es requerido")

        result = self.repository.delete(alcaldia_id)
        logger.info(f"=== USE CASE: Alcaldia deleted: {alcaldia_id} ===")

        return result
