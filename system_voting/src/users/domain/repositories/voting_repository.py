from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.voting import (
    PopularConsultation,
    VotingOption,
    Vote,
    VotingPermission,
    CreateConsultationCommand,
    UpdateConsultationCommand,
    CreateVotingOptionCommand,
    VoteCommand,
    GrantVotingPermissionCommand,
    VotingResults,
    EligibleVoter,
    VotingEligibilityCheck
)


class VotingRepositoryPort(ABC):
    """Puerto del repositorio de votación - Arquitectura Hexagonal"""
    
    # ============================================
    # CONSULTAS POPULARES
    # ============================================
    
    @abstractmethod
    def create_consultation(self, command: CreateConsultationCommand) -> PopularConsultation:
        """Crear una nueva consulta popular"""
        pass
    
    @abstractmethod
    def get_consultation(self, consultation_id: str) -> Optional[PopularConsultation]:
        """Obtener una consulta por ID"""
        pass
    
    @abstractmethod
    def get_consultations(self, status: Optional[str] = None, limit: int = 50) -> List[PopularConsultation]:
        """Obtener lista de consultas populares"""
        pass
    
    @abstractmethod
    def update_consultation(self, command: UpdateConsultationCommand) -> Optional[PopularConsultation]:
        """Actualizar una consulta popular"""
        pass
    
    @abstractmethod
    def delete_consultation(self, consultation_id: str) -> bool:
        """Eliminar una consulta popular"""
        pass
    
    @abstractmethod
    def get_active_consultations(self) -> List[PopularConsultation]:
        """Obtener consultas activas"""
        pass
    
    # ============================================
    # OPCIONES DE VOTACIÓN
    # ============================================
    
    @abstractmethod
    def create_voting_option(self, command: CreateVotingOptionCommand) -> VotingOption:
        """Crear una opción de votación"""
        pass
    
    @abstractmethod
    def get_consultation_options(self, consultation_id: str) -> List[VotingOption]:
        """Obtener opciones de una consulta"""
        pass
    
    @abstractmethod
    def update_voting_option(self, option_id: str, data: Dict[str, Any]) -> Optional[VotingOption]:
        """Actualizar una opción de votación"""
        pass
    
    @abstractmethod
    def delete_voting_option(self, option_id: str) -> bool:
        """Eliminar una opción de votación"""
        pass
    
    # ============================================
    # VOTOS
    # ============================================
    
    @abstractmethod
    def cast_vote(self, command: VoteCommand) -> Vote:
        """Registrar un voto"""
        pass
    
    @abstractmethod
    def get_user_votes(self, user_id: str) -> List[Vote]:
        """Obtener votos de un usuario"""
        pass
    
    @abstractmethod
    def get_consultation_votes(self, consultation_id: str) -> List[Vote]:
        """Obtener votos de una consulta"""
        pass
    
    @abstractmethod
    def has_user_voted(self, user_id: str, consultation_id: str) -> bool:
        """Verificar si un usuario ya votó en una consulta"""
        pass
    
    @abstractmethod
    def get_vote_count(self, consultation_id: str, option_id: str = None) -> int:
        """Obtener conteo de votos"""
        pass
    
    # ============================================
    # PERMISOS DE VOTACIÓN
    # ============================================
    
    @abstractmethod
    def grant_voting_permission(self, command: GrantVotingPermissionCommand) -> VotingPermission:
        """Otorgar permiso de votación"""
        pass
    
    @abstractmethod
    def revoke_voting_permission(self, user_id: str, consultation_id: str) -> bool:
        """Revocar permiso de votación"""
        pass
    
    @abstractmethod
    def get_user_voting_permission(self, user_id: str, consultation_id: str) -> Optional[VotingPermission]:
        """Obtener permiso de votación de un usuario"""
        pass
    
    @abstractmethod
    def get_consultation_permissions(self, consultation_id: str) -> List[VotingPermission]:
        """Obtener permisos de una consulta"""
        pass
    
    @abstractmethod
    def check_voting_eligibility(self, user_id: str, consultation_id: str) -> VotingEligibilityCheck:
        """Verificar elegibilidad para votar"""
        pass
    
    # ============================================
    # RESULTADOS Y ESTADÍSTICAS
    # ============================================
    
    @abstractmethod
    def get_consultation_results(self, consultation_id: str) -> VotingResults:
        """Obtener resultados de una consulta"""
        pass
    
    @abstractmethod
    def get_eligible_voters(self, consultation_id: str) -> List[EligibleVoter]:
        """Obtener votantes elegibles para una consulta"""
        pass
    
    @abstractmethod
    def get_voting_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas generales de votación"""
        pass
    
    # ============================================
    # VALIDACIONES DE NEGOCIO
    # ============================================
    
    @abstractmethod
    def validate_consultation_dates(self, start_date: datetime, end_date: datetime) -> bool:
        """Validar fechas de consulta"""
        pass
    
    @abstractmethod
    def can_user_vote_in_consultation(self, user_id: str, consultation_id: str) -> bool:
        """Verificar si un usuario puede votar en una consulta"""
        pass
    
    @abstractmethod
    def is_user_party_member(self, user_id: str) -> bool:
        """Verificar si un usuario es miembro de partido político"""
        pass
