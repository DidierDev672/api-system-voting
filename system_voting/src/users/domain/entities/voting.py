from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class ConsultationStatus(Enum):
    """Estados de una consulta popular"""
    ACTIVE = "ACTIVE"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"


@dataclass
class VotingOption:
    """Opción de votación para una consulta popular"""
    id: Optional[str] = None
    consultation_id: str = ""
    title: str = ""
    description: Optional[str] = None
    order_index: int = 0
    votes_count: int = 0
    created_at: Optional[datetime] = None


@dataclass
class PopularConsultation:
    """Consulta popular de votación"""
    id: Optional[str] = None
    title: str = ""
    description: str = ""
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    status: ConsultationStatus = ConsultationStatus.ACTIVE
    min_votes: int = 1
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Propiedades calculadas
    options: List[VotingOption] = field(default_factory=list)
    total_votes: int = 0
    total_options: int = 0
    
    def is_active(self) -> bool:
        """Verificar si la consulta está activa"""
        now = datetime.now()
        return (
            self.status == ConsultationStatus.ACTIVE and
            self.start_date <= now and
            (self.end_date is None or self.end_date > now)
        )
    
    def is_finished(self) -> bool:
        """Verificar si la consulta ha finalizado"""
        if self.status in [ConsultationStatus.FINISHED, ConsultationStatus.CANCELLED]:
            return True
        if self.end_date and self.end_date <= datetime.now():
            return True
        return False
    
    def can_vote(self) -> bool:
        """Verificar si se puede votar en esta consulta"""
        return self.is_active()


@dataclass
class Vote:
    """Voto de un usuario en una consulta popular"""
    id: Optional[str] = None
    consultation_id: str = ""
    option_id: str = ""
    user_id: str = ""
    party_member_id: Optional[str] = None
    voted_at: datetime = field(default_factory=datetime.now)


@dataclass
class VotingPermission:
    """Permiso de votación para un usuario en una consulta"""
    id: Optional[str] = None
    user_id: str = ""
    consultation_id: str = ""
    can_vote: bool = False
    granted_by: Optional[str] = None
    granted_at: Optional[datetime] = None


@dataclass
class CreateConsultationCommand:
    """Comando para crear una consulta popular"""
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    min_votes: int = 1
    created_by: str = ""


@dataclass
class UpdateConsultationCommand:
    """Comando para actualizar una consulta popular"""
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[ConsultationStatus] = None
    min_votes: Optional[int] = None


@dataclass
class CreateVotingOptionCommand:
    """Comando para crear una opción de votación"""
    consultation_id: str
    title: str
    description: Optional[str] = None
    order_index: int = 0


@dataclass
class VoteCommand:
    """Comando para registrar un voto"""
    consultation_id: str
    option_id: str
    user_id: str
    party_member_id: Optional[str] = None


@dataclass
class GrantVotingPermissionCommand:
    """Comando para otorgar permiso de votación"""
    user_id: str
    consultation_id: str
    can_vote: bool = True
    granted_by: str = ""


@dataclass
class VotingResults:
    """Resultados de una consulta popular"""
    consultation_id: str
    consultation_title: str
    total_votes: int
    options: List[dict] = field(default_factory=list)
    
    def add_option_result(self, option_id: str, title: str, votes: int, percentage: float):
        """Agregar resultado de una opción"""
        self.options.append({
            "option_id": option_id,
            "title": title,
            "votes": votes,
            "percentage": percentage
        })
    
    def get_winner(self) -> Optional[dict]:
        """Obtener la opción ganadora"""
        if not self.options:
            return None
        return max(self.options, key=lambda x: x["votes"])


@dataclass
class EligibleVoter:
    """Votante elegible para participar"""
    user_id: str
    full_name: str
    email: str
    party_member_id: Optional[str] = None
    party_id: Optional[str] = None
    party_name: Optional[str] = None
    consultation_id: Optional[str] = None
    can_vote: bool = True
    
    def is_party_member(self) -> bool:
        """Verificar si es miembro de partido político"""
        return self.party_member_id is not None
    
    def has_voting_permission(self) -> bool:
        """Verificar si tiene permiso de votación"""
        return self.can_vote
    
    def can_participate(self) -> bool:
        """Verificar si puede participar en votación"""
        return self.is_party_member() and self.has_voting_permission()


@dataclass
class VotingEligibilityCheck:
    """Resultado de verificación de elegibilidad para votar"""
    user_id: str
    consultation_id: str
    is_eligible: bool
    reasons: List[str] = field(default_factory=list)
    
    def add_reason(self, reason: str):
        """Agregar razón de no elegibilidad"""
        self.reasons.append(reason)
        self.is_eligible = False
    
    def is_party_member(self) -> bool:
        """Verificar si es miembro de partido"""
        return "No es miembro de partido político" not in self.reasons
    
    def has_permission(self) -> bool:
        """Verificar si tiene permiso"""
        return "No tiene permiso de votación" not in self.reasons
    
    def has_voted(self) -> bool:
        """Verificar si ya votó"""
        return "Ya ha votado en esta consulta" not in self.reasons
