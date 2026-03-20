"""
Entity - Alcaldia
Domain Layer
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Alcaldia:
    """Alcaldia Entity - Represents a municipality/mayor's office"""

    id: str
    nombre_entidad: str
    nit: str
    codigo_sigep: str
    orden_entidad: str  # "Municipal" o "Distrital"
    municipio: str
    direccion_fisica: str
    dominio: str
    correo_institucional: str
    id_alcalde: str  # FK to party_members
    nombre_alcalde: str  # Nombre completo del alcalde
    acto_posesion: str  # Numero de acta o decreto
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.orden_entidad not in ["Municipal", "Distrital"]:
            raise ValueError("orden_entidad debe ser 'Municipal' o 'Distrital'")


@dataclass
class CreateAlcaldiaDTO:
    """DTO for creating a new alcaldia"""

    nombre_entidad: str
    nit: str
    codigo_sigep: str
    orden_entidad: str
    municipio: str
    direccion_fisica: str
    dominio: str
    correo_institucional: str
    id_alcalde: str
    nombre_alcalde: str
    acto_posesion: str


@dataclass
class UpdateAlcaldiaDTO:
    """DTO for updating an alcaldia"""

    nombre_entidad: Optional[str] = None
    nit: Optional[str] = None
    codigo_sigep: Optional[str] = None
    orden_entidad: Optional[str] = None
    municipio: Optional[str] = None
    direccion_fisica: Optional[str] = None
    dominio: Optional[str] = None
    correo_institucional: Optional[str] = None
    id_alcalde: Optional[str] = None
    nombre_alcalde: Optional[str] = None
    acto_posesion: Optional[str] = None
