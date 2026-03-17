"""
Domain Entities - Municipal Council Secretary
Vertical Slicing + SOLID Principles
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class MunicipalCouncilSecretary:
    id: str
    full_name: str
    document_type: str
    document_id: str
    exact_position: str  # Cargo exacto: Secretario General o Secretario de comision
    administrative_act: str  # Acto administrativo de eleccion
    possession_date: str  # Fecha de posesion
    legal_period: str  # Perido legal
    performance_type: str  # Calidad de actuacion: ad-hoc, temporal
    institutional_email: str  # Correo institucional
    professional_title: Optional[str] = None  # Titulo profesional
    digital_signature: Optional[str] = None  # Firma digital
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateMunicipalCouncilSecretaryDTO:
    full_name: str
    document_type: str
    document_id: str
    exact_position: str
    administrative_act: str
    possession_date: str
    legal_period: str
    performance_type: str
    institutional_email: str
    professional_title: Optional[str] = None
    digital_signature: Optional[str] = None
