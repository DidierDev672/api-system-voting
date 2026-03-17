"""
Domain Entities - Municipal Council Session
Vertical Slicing + SOLID Principles
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class MunicipalCouncilSession:
    id: str
    title_session: str
    type_session: str
    status_session: str
    date_hour_start: str
    date_hour_end: str
    modality: str  # presencial, virtual, hibrida
    place_enclosure: str
    orden_day: str
    quorum_required: int
    id_president: str
    id_secretary: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CreateMunicipalCouncilSessionDTO:
    title_session: str
    type_session: str
    status_session: str
    date_hour_start: str
    date_hour_end: str
    modality: str
    place_enclosure: str
    orden_day: str
    quorum_required: int
    id_president: str
    id_secretary: str
