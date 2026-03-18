from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from ..value_objects.tipo_curul import TipoCurul, ComisionPermanente


@dataclass
class Bancada:
    id_miembro: str
    id_partido: str
    tipo_curul: TipoCurul
    fin_periodo: date
    declaraciones_bienes: str
    antecedentes_siri_sirus: str
    comision_permanente: ComisionPermanente
    correo_institucional: str
    profesion: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True

    def validate(self) -> None:
        if not self.id_miembro:
            raise ValueError("El miembro es requerido")
        if len(self.id_miembro) != 36:
            raise ValueError("El ID del miembro debe ser un UUID válido")
        if not self.id_partido:
            raise ValueError("El partido es requerido")
        if len(self.id_partido) != 36:
            raise ValueError("El ID del partido debe ser un UUID válido")
        if not self.correo_institucional:
            raise ValueError("El correo institucional es requerido")
        if not self.profesion:
            raise ValueError("La profesión es requerida")

    def is_activa(self) -> bool:
        return self.fin_periodo >= date.today()

    def verificar_habilitado(self) -> bool:
        return self.antecedentes_siri_sirus.upper() in [
            "SIN ANTECEDENTES",
            "N/A",
            "LIMPIO",
        ]
