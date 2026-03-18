from enum import Enum


class TipoCurul(str, Enum):
    ORDINARIA = "Ordinaria"
    ESTATUTO_OPOSICION = "Estatuto de Oposición"
    REEMPLAZO = "Reemplazo"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    @classmethod
    def values(cls):
        return [item.value for item in cls]


class ComisionPermanente(str, Enum):
    PRESUPUESTO = "Comisión de Presupuesto"
    PLAN_DESARROLLO = "Comisión de Plan de Desarrollo"
    GOBIERNO = "Comisión de Gobierno"
    HACIENDA = "Comisión de Hacienda"
    EDUCACION = "Comisión de Educación"
    SALUD = "Comisión de Salud"
    INFRAESTRUCTURA = "Comisión de Infraestructura"
    AGRICULTURA = "Comisión de Agricultura"
    AMBIENTE = "Comisión de Ambiente"
    PARTICIPACION = "Comisión de Participación Ciudadana"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]

    @classmethod
    def values(cls):
        return [item.value for item in cls]
