from typing import List, Optional
import logging
from system_voting.src.bancada.domain.entities.bancada import Bancada
from system_voting.src.bancada.domain.ports.bancada_repository import (
    BancadaRepositoryInterface,
)
from system_voting.src.bancada.domain.value_objects.tipo_curul import (
    TipoCurul,
    ComisionPermanente,
)
from supabase_integration import get_bancada_service

logger = logging.getLogger(__name__)


class SupabaseBancadaRepository(BancadaRepositoryInterface):
    """Adapter - Implementación del repositorio usando Supabase"""

    def __init__(self):
        self.service = get_bancada_service()

    def _to_dict(self, bancada: Bancada) -> dict:
        """Convertir entity a diccionario para Supabase"""
        tipo_curul_value = (
            bancada.tipo_curul.value
            if hasattr(bancada.tipo_curul, "value")
            else bancada.tipo_curul
        )
        comision_value = (
            bancada.comision_permanente.value
            if hasattr(bancada.comision_permanente, "value")
            else bancada.comision_permanente
        )

        return {
            "id_miembro": bancada.id_miembro,
            "id_partido": bancada.id_partido,
            "tipo_curul": tipo_curul_value,
            "fin_periodo": str(bancada.fin_periodo),
            "declaraciones_bienes": bancada.declaraciones_bienes,
            "antecedentes_siri_sirus": bancada.antecedentes_siri_sirus,
            "comision_permanente": comision_value,
            "correo_institucional": bancada.correo_institucional,
            "profesion": bancada.profesion,
        }

    def _from_dict(self, data: dict) -> Bancada:
        """Convertir diccionario de Supabase a entity"""
        return Bancada(
            id=data.get("id"),
            id_miembro=data.get("id_miembro"),
            id_partido=data.get("id_partido"),
            tipo_curul=TipoCurul(data.get("tipo_curul")),
            fin_periodo=data.get("fin_periodo"),
            declaraciones_bienes=data.get("declaraciones_bienes", ""),
            antecedentes_siri_sirus=data.get("antecedentes_siri_sirus", ""),
            comision_permanente=ComisionPermanente(data.get("comision_permanente")),
            correo_institucional=data.get("correo_institucional"),
            profesion=data.get("profesion"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def get_all(self) -> List[Bancada]:
        try:
            records = self.service.get_all_records()
            return [self._from_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Error en get_all: {str(e)}")
            return []

    def get_by_id(self, id: str) -> Optional[Bancada]:
        try:
            record = self.service.get_record_by_id(id)
            return self._from_dict(record) if record else None
        except Exception as e:
            logger.error(f"Error en get_by_id: {str(e)}")
            return None

    def get_by_miembro(self, id_miembro: str) -> List[Bancada]:
        try:
            records = self.service.get_by_miembro(id_miembro)
            return [self._from_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Error en get_by_miembro: {str(e)}")
            return []

    def get_by_partido(self, id_partido: str) -> List[Bancada]:
        try:
            records = self.service.get_by_partido(id_partido)
            return [self._from_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Error en get_by_partido: {str(e)}")
            return []

    def create(self, bancada: Bancada) -> Bancada:
        try:
            bancada.validate()
            data = self._to_dict(bancada)
            result = self.service.create_record(data)
            return self._from_dict(result)
        except Exception as e:
            logger.error(f"Error en create: {str(e)}")
            raise

    def update(self, id: str, bancada: Bancada) -> Bancada:
        try:
            bancada.validate()
            data = self._to_dict(bancada)
            result = self.service.update_record(id, data)
            return self._from_dict(result)
        except Exception as e:
            logger.error(f"Error en update: {str(e)}")
            raise

    def delete(self, id: str) -> bool:
        try:
            self.service.delete_record(id)
            return True
        except Exception as e:
            logger.error(f"Error en delete: {str(e)}")
            return False
