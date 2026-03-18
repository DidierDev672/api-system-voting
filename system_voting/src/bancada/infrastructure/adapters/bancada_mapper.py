import uuid
from system_voting.src.bancada.domain.entities.bancada import Bancada
from system_voting.src.bancada.domain.value_objects.tipo_curul import (
    TipoCurul,
    ComisionPermanente,
)
from system_voting.src.bancada.infrastructure.models.bancada_model import BancadaModel


class BancadaMapper:
    """Mapper para convertir entre Dominio y Modelo Django (Mappers Pattern)"""

    @staticmethod
    def to_domain(model: BancadaModel) -> Bancada:
        return Bancada(
            id=str(model.id),
            id_miembro=str(model.id_miembro),
            id_partido=str(model.id_partido),
            tipo_curul=TipoCurul(model.tipo_curul),
            fin_periodo=model.fin_periodo,
            declaraciones_bienes=model.declaraciones_bienes,
            antecedentes_siri_sirus=model.antecedentes_siri_sirus,
            comision_permanente=ComisionPermanente(model.comision_permanente),
            correo_institucional=model.correo_institucional,
            profesion=model.profesion,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(bancada: Bancada) -> BancadaModel:
        tipo_curul_value = (
            bancada.tipo_curul.value
            if isinstance(bancada.tipo_curul, TipoCurul)
            else bancada.tipo_curul
        )
        comision_value = (
            bancada.comision_permanente.value
            if isinstance(bancada.comision_permanente, ComisionPermanente)
            else bancada.comision_permanente
        )

        model = BancadaModel(
            id_miembro=uuid.UUID(bancada.id_miembro)
            if bancada.id_miembro
            else uuid.uuid4(),
            id_partido=uuid.UUID(bancada.id_partido)
            if bancada.id_partido
            else uuid.uuid4(),
            tipo_curul=tipo_curul_value,
            fin_periodo=bancada.fin_periodo,
            declaraciones_bienes=bancada.declaraciones_bienes,
            antecedentes_siri_sirus=bancada.antecedentes_siri_sirus,
            comision_permanente=comision_value,
            correo_institucional=bancada.correo_institucional,
            profesion=bancada.profesion,
        )

        if bancada.id:
            try:
                model.id = uuid.UUID(bancada.id)
            except (ValueError, AttributeError):
                pass

        return model
