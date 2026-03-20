"""
Repository Adapter - Alcaldia
Infrastructure Layer - Supabase Implementation
SOLID Principles - Adapter Pattern
"""

import uuid
import logging
from typing import List, Optional
from supabase_integration import SupabaseService as BaseSupabaseService
from system_voting.src.alcaldia.domain.entities.alcaldia import (
    Alcaldia,
    CreateAlcaldiaDTO,
    UpdateAlcaldiaDTO,
)
from system_voting.src.alcaldia.domain.ports.alcaldia_repository import (
    AlcaldiaRepositoryPort,
)

logger = logging.getLogger(__name__)


class SupabaseAlcaldiaRepository(AlcaldiaRepositoryPort):
    """Supabase implementation of AlcaldiaRepositoryPort"""

    def __init__(self):
        self.supabase_service = BaseSupabaseService()
        self.table_name = "alcaldias"

    def _map_to_entity(self, data: dict) -> Alcaldia:
        """Map database response to Alcaldia entity"""
        return Alcaldia(
            id=data.get("id", ""),
            nombre_entidad=data.get("nombre_entidad", ""),
            nit=data.get("nit", ""),
            codigo_sigep=data.get("codigo_sigep", ""),
            orden_entidad=data.get("orden_entidad", ""),
            municipio=data.get("municipio", ""),
            direccion_fisica=data.get("direccion_fisica", ""),
            dominio=data.get("dominio", ""),
            correo_institucional=data.get("correo_institucional", ""),
            id_alcalde=data.get("id_alcalde", ""),
            nombre_alcalde=data.get("nombre_alcalde", ""),
            acto_posesion=data.get("acto_posesion", ""),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def create(self, data: CreateAlcaldiaDTO) -> Alcaldia:
        """Create a new alcaldia"""
        logger.info(f"=== REPOSITORY: Creating alcaldia: {data.nombre_entidad} ===")

        alcaldia_id = str(uuid.uuid4())

        db_data = {
            "id": alcaldia_id,
            "nombre_entidad": data.nombre_entidad,
            "nit": data.nit,
            "codigo_sigep": data.codigo_sigep,
            "orden_entidad": data.orden_entidad,
            "municipio": data.municipio,
            "direccion_fisica": data.direccion_fisica,
            "dominio": data.dominio,
            "correo_institucional": data.correo_institucional,
            "id_alcalde": data.id_alcalde,
            "nombre_alcalde": data.nombre_alcalde,
            "acto_posesion": data.acto_posesion,
        }

        result = self.supabase_service.insert_record(self.table_name, db_data)
        logger.info(f"=== REPOSITORY: Alcaldia created: {result} ===")

        return self._map_to_entity(result)

    def get_all(self) -> List[Alcaldia]:
        """Get all alcaldias"""
        logger.info("=== REPOSITORY: Getting all alcaldias ===")

        results = self.supabase_service.get_all_records(self.table_name, {})

        alcaldias = [self._map_to_entity(r) for r in (results or [])]
        logger.info(f"=== REPOSITORY: Found {len(alcaldias)} alcaldias ===")

        return alcaldias

    def get_by_id(self, alcaldia_id: str) -> Optional[Alcaldia]:
        """Get alcaldia by ID"""
        logger.info(f"=== REPOSITORY: Getting alcaldia by ID: {alcaldia_id} ===")

        result = self.supabase_service.get_record_by_id(self.table_name, alcaldia_id)

        if not result:
            return None

        return self._map_to_entity(result)

    def update(self, alcaldia_id: str, data: UpdateAlcaldiaDTO) -> Alcaldia:
        """Update an alcaldia"""
        logger.info(f"=== REPOSITORY: Updating alcaldia: {alcaldia_id} ===")

        update_data = {}

        if data.nombre_entidad is not None:
            update_data["nombre_entidad"] = data.nombre_entidad
        if data.nit is not None:
            update_data["nit"] = data.nit
        if data.codigo_sigep is not None:
            update_data["codigo_sigep"] = data.codigo_sigep
        if data.orden_entidad is not None:
            update_data["orden_entidad"] = data.orden_entidad
        if data.municipio is not None:
            update_data["municipio"] = data.municipio
        if data.direccion_fisica is not None:
            update_data["direccion_fisica"] = data.direccion_fisica
        if data.dominio is not None:
            update_data["dominio"] = data.dominio
        if data.correo_institucional is not None:
            update_data["correo_institucional"] = data.correo_institucional
        if data.id_alcalde is not None:
            update_data["id_alcalde"] = data.id_alcalde
        if data.nombre_alcalde is not None:
            update_data["nombre_alcalde"] = data.nombre_alcalde
        if data.acto_posesion is not None:
            update_data["acto_posesion"] = data.acto_posesion

        result = self.supabase_service.update_record(
            self.table_name, alcaldia_id, update_data
        )

        return self._map_to_entity(result)

    def delete(self, alcaldia_id: str) -> bool:
        """Delete an alcaldia"""
        logger.info(f"=== REPOSITORY: Deleting alcaldia: {alcaldia_id} ===")

        result = self.supabase_service.delete_record(self.table_name, alcaldia_id)

        return result
