import uuid
from typing import List, Optional
from system_voting.src.bancada.domain.entities.bancada import Bancada
from system_voting.src.bancada.domain.ports.bancada_repository import (
    BancadaRepositoryInterface,
)
from system_voting.src.bancada.infrastructure.models.bancada_model import BancadaModel
from .bancada_mapper import BancadaMapper


class BancadaRepository(BancadaRepositoryInterface):
    """Adapter - Implementación del repositorio usando Django ORM"""

    def get_all(self) -> List[Bancada]:
        models = BancadaModel.objects.all()
        return [BancadaMapper.to_domain(model) for model in models]

    def get_by_id(self, id: str) -> Optional[Bancada]:
        try:
            model = BancadaModel.objects.get(id=uuid.UUID(id))
            return BancadaMapper.to_domain(model)
        except BancadaModel.DoesNotExist:
            return None
        except ValueError:
            return None

    def get_by_miembro(self, id_miembro: str) -> List[Bancada]:
        try:
            models = BancadaModel.objects.filter(id_miembro=uuid.UUID(id_miembro))
            return [BancadaMapper.to_domain(model) for model in models]
        except ValueError:
            return []

    def get_by_partido(self, id_partido: str) -> List[Bancada]:
        try:
            models = BancadaModel.objects.filter(id_partido=uuid.UUID(id_partido))
            return [BancadaMapper.to_domain(model) for model in models]
        except ValueError:
            return []

    def create(self, bancada: Bancada) -> Bancada:
        bancada.validate()
        model = BancadaMapper.to_model(bancada)
        model.save()
        return BancadaMapper.to_domain(model)

    def update(self, id: str, bancada: Bancada) -> Bancada:
        try:
            model = BancadaModel.objects.get(id=uuid.UUID(id))
            model.id_miembro = (
                uuid.UUID(bancada.id_miembro) if bancada.id_miembro else None
            )
            model.id_partido = (
                uuid.UUID(bancada.id_partido) if bancada.id_partido else None
            )
            model.tipo_curul = (
                bancada.tipo_curul.value
                if hasattr(bancada.tipo_curul, "value")
                else bancada.tipo_curul
            )
            model.fin_periodo = bancada.fin_periodo
            model.declaraciones_bienes = bancada.declaraciones_bienes
            model.antecedentes_siri_sirus = bancada.antecedentes_siri_sirus
            model.comision_permanente = (
                bancada.comision_permanente.value
                if hasattr(bancada.comision_permanente, "value")
                else bancada.comision_permanente
            )
            model.correo_institucional = bancada.correo_institucional
            model.profesion = bancada.profesion
            model.save()
            return BancadaMapper.to_domain(model)
        except BancadaModel.DoesNotExist:
            raise ValueError(f"Bancada con ID {id} no existe")
        except ValueError:
            raise ValueError(f"ID inválido: {id}")

    def delete(self, id: str) -> bool:
        try:
            model = BancadaModel.objects.get(id=uuid.UUID(id))
            model.delete()
            return True
        except BancadaModel.DoesNotExist:
            return False
        except ValueError:
            return False
