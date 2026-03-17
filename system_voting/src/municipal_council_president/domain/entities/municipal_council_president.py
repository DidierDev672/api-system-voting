"""
Domain Entities - Municipal Council President
Vertical Slicing + SOLID Principles
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class MunicipalCouncilPresident:
    id: str
    full_name: str
    document_type: str  # Tipo de documento (CI, Pasaporte, etc.)
    document_id: str  # Documento de identidad
    board_position: str  # Cargo de la mesa
    political_party: str  # Partido politico
    election_period: str  # Periodo de eleccion
    presidency_type: str  # Calidad de presidencia
    position_time: str  # Hora de toma de posicion
    institutional_email: str  # Correo institucional
    digital_signature: Optional[str] = None  # Firma digital
    fingerprint: Optional[str] = None  # Huella digital
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateMunicipalCouncilPresidentDTO:
    full_name: str
    document_type: str
    document_id: str
    board_position: str
    political_party: str
    election_period: str
    presidency_type: str
    position_time: str
    institutional_email: str
    digital_signature: Optional[str] = None
    fingerprint: Optional[str] = None
