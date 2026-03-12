from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ...domain.repositories.voting_repository import VotingRepositoryPort
from ...domain.entities.voting import (
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
    VotingEligibilityCheck,
    ConsultationStatus
)


class VotingService:
    """Servicio de aplicación para gestión de votación - Vertical Slicing"""
    
    def __init__(self, voting_repository: VotingRepositoryPort):
        self.voting_repository = voting_repository
    
    # ============================================
    # GESTIÓN DE CONSULTAS POPULARES
    # ============================================
    
    def create_consultation(self, command: CreateConsultationCommand) -> PopularConsultation:
        """Crear una nueva consulta popular"""
        # Validaciones de negocio
        self._validate_consultation_creation(command)
        
        # Crear consulta
        consultation = self.voting_repository.create_consultation(command)
        
        return consultation
    
    def update_consultation(self, command: UpdateConsultationCommand) -> Optional[PopularConsultation]:
        """Actualizar una consulta popular"""
        # Verificar que la consulta existe
        existing = self.voting_repository.get_consultation(command.id)
        if not existing:
            raise ValueError("La consulta no existe")
        
        # Validar que no haya votos si se modifican fechas
        if command.start_date or command.end_date:
            vote_count = self.voting_repository.get_vote_count(command.id)
            if vote_count > 0:
                raise ValueError("No se pueden modificar las fechas de una consulta que ya tiene votos")
        
        # Actualizar consulta
        return self.voting_repository.update_consultation(command)
    
    def delete_consultation(self, consultation_id: str) -> bool:
        """Eliminar una consulta popular"""
        # Verificar que la consulta existe
        consultation = self.voting_repository.get_consultation(consultation_id)
        if not consultation:
            raise ValueError("La consulta no existe")
        
        # Verificar que no haya votos
        vote_count = self.voting_repository.get_vote_count(consultation_id)
        if vote_count > 0:
            raise ValueError("No se puede eliminar una consulta que ya tiene votos")
        
        return self.voting_repository.delete_consultation(consultation_id)
    
    def get_consultation(self, consultation_id: str) -> Optional[PopularConsultation]:
        """Obtener una consulta por ID"""
        return self.voting_repository.get_consultation(consultation_id)
    
    def get_active_consultations(self) -> List[PopularConsultation]:
        """Obtener consultas activas para votación"""
        return self.voting_repository.get_active_consultations()
    
    def get_consultations(self, status: Optional[str] = None, limit: int = 50) -> List[PopularConsultation]:
        """Obtener lista de consultas populares"""
        return self.voting_repository.get_consultations(status, limit)
    
    def finish_consultation(self, consultation_id: str) -> bool:
        """Finalizar una consulta popular"""
        consultation = self.voting_repository.get_consultation(consultation_id)
        if not consultation:
            raise ValueError("La consulta no existe")
        
        if consultation.status == ConsultationStatus.FINISHED:
            raise ValueError("La consulta ya está finalizada")
        
        # Verificar que tenga el mínimo de votos
        vote_count = self.voting_repository.get_vote_count(consultation_id)
        if vote_count < consultation.min_votes:
            raise ValueError(f"La consulta no tiene el mínimo de votos requeridos ({consultation.min_votes})")
        
        # Actualizar estado
        command = UpdateConsultationCommand(
            id=consultation_id,
            status=ConsultationStatus.FINISHED
        )
        
        result = self.voting_repository.update_consultation(command)
        return result is not None
    
    # ============================================
    # GESTIÓN DE OPCIONES DE VOTACIÓN
    # ============================================
    
    def add_voting_option(self, command: CreateVotingOptionCommand) -> VotingOption:
        """Agregar una opción de votación a una consulta"""
        # Verificar que la consulta existe
        consultation = self.voting_repository.get_consultation(command.consultation_id)
        if not consultation:
            raise ValueError("La consulta no existe")
        
        # Verificar que la consulta esté activa
        if consultation.status != ConsultationStatus.ACTIVE:
            raise ValueError("No se pueden agregar opciones a consultas que no están activas")
        
        # Verificar que no haya votos
        vote_count = self.voting_repository.get_vote_count(command.consultation_id)
        if vote_count > 0:
            raise ValueError("No se pueden agregar opciones a consultas que ya tienen votos")
        
        # Verificar límite de opciones (máximo 10)
        existing_options = self.voting_repository.get_consultation_options(command.consultation_id)
        if len(existing_options) >= 10:
            raise ValueError("Una consulta no puede tener más de 10 opciones")
        
        # Crear opción
        return self.voting_repository.create_voting_option(command)
    
    def remove_voting_option(self, option_id: str) -> bool:
        """Eliminar una opción de votación"""
        # Obtener la opción para verificar la consulta
        options = self.voting_repository.get_consultation_options("")
        option = next((o for o in options if o.id == option_id), None)
        
        if not option:
            raise ValueError("La opción no existe")
        
        # Verificar que no haya votos en esta opción
        vote_count = self.voting_repository.get_vote_count(option.consultation_id, option_id)
        if vote_count > 0:
            raise ValueError("No se puede eliminar una opción que ya tiene votos")
        
        return self.voting_repository.delete_voting_option(option_id)
    
    # ============================================
    # GESTIÓN DE VOTOS
    # ============================================
    
    def cast_vote(self, command: VoteCommand) -> Vote:
        """Registrar un voto de un usuario"""
        # Verificar elegibilidad
        eligibility = self.voting_repository.check_voting_eligibility(command.user_id, command.consultation_id)
        if not eligibility.is_eligible:
            raise ValueError(f"No puede votar: {', '.join(eligibility.reasons)}")
        
        # Verificar que la opción exista
        options = self.voting_repository.get_consultation_options(command.consultation_id)
        option = next((o for o in options if o.id == command.option_id), None)
        if not option:
            raise ValueError("La opción de votación no existe")
        
        # Registrar voto
        vote = self.voting_repository.cast_vote(command)
        
        # Verificar si se alcanzó el mínimo de votos para finalizar
        consultation = self.voting_repository.get_consultation(command.consultation_id)
        total_votes = self.voting_repository.get_vote_count(command.consultation_id)
        
        if total_votes >= consultation.min_votes:
            # Auto-finalizar la consulta
            self.finish_consultation(command.consultation_id)
        
        return vote
    
    def get_user_votes(self, user_id: str) -> List[Vote]:
        """Obtener el historial de votos de un usuario"""
        return self.voting_repository.get_user_votes(user_id)
    
    def has_user_voted(self, user_id: str, consultation_id: str) -> bool:
        """Verificar si un usuario ya votó en una consulta"""
        return self.voting_repository.has_user_voted(user_id, consultation_id)
    
    # ============================================
    # GESTIÓN DE PERMISOS DE VOTACIÓN
    # ============================================
    
    def grant_voting_permission(self, command: GrantVotingPermissionCommand) -> VotingPermission:
        """Otorgar permiso de votación a un usuario"""
        # Verificar que la consulta existe
        consultation = self.voting_repository.get_consultation(command.consultation_id)
        if not consultation:
            raise ValueError("La consulta no existe")
        
        # Verificar que el usuario sea miembro de partido
        if not self.voting_repository.is_user_party_member(command.user_id):
            raise ValueError("El usuario no es miembro de ningún partido político")
        
        # Verificar que el usuario que otorga el permiso tenga autorización
        # (Esta validación podría depender de roles específicos)
        
        return self.voting_repository.grant_voting_permission(command)
    
    def revoke_voting_permission(self, user_id: str, consultation_id: str) -> bool:
        """Revocar permiso de votación de un usuario"""
        # Verificar que exista el permiso
        permission = self.voting_repository.get_user_voting_permission(user_id, consultation_id)
        if not permission:
            raise ValueError("El usuario no tiene permiso de votación en esta consulta")
        
        return self.voting_repository.revoke_voting_permission(user_id, consultation_id)
    
    def get_user_voting_permission(self, user_id: str, consultation_id: str) -> Optional[VotingPermission]:
        """Obtener permiso de votación de un usuario"""
        return self.voting_repository.get_user_voting_permission(user_id, consultation_id)
    
    def get_eligible_voters(self, consultation_id: str) -> List[EligibleVoter]:
        """Obtener lista de votantes elegibles para una consulta"""
        return self.voting_repository.get_eligible_voters(consultation_id)
    
    # ============================================
    # RESULTADOS Y ESTADÍSTICAS
    # ============================================
    
    def get_consultation_results(self, consultation_id: str) -> VotingResults:
        """Obtener resultados de una consulta popular"""
        return self.voting_repository.get_consultation_results(consultation_id)
    
    def get_voting_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas generales del sistema de votación"""
        return self.voting_repository.get_voting_statistics()
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Obtener datos para el dashboard de votación"""
        stats = self.get_voting_statistics()
        
        # Consultas recientes
        recent_consultations = self.get_consultations(limit=5)
        
        # Consultas activas
        active_consultations = self.get_active_consultations()
        
        return {
            "statistics": stats,
            "recent_consultations": [
                {
                    "id": c.id,
                    "title": c.title,
                    "status": c.status.value,
                    "total_votes": c.total_votes,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                }
                for c in recent_consultations
            ],
            "active_consultations": [
                {
                    "id": c.id,
                    "title": c.title,
                    "end_date": c.end_date.isoformat() if c.end_date else None,
                    "total_votes": c.total_votes,
                    "total_options": c.total_options
                }
                for c in active_consultations
            ]
        }
    
    # ============================================
    # VALIDACIONES DE NEGOCIO
    # ============================================
    
    def _validate_consultation_creation(self, command: CreateConsultationCommand):
        """Validar la creación de una consulta popular"""
        # Validar título
        if not command.title or len(command.title.strip()) < 10:
            raise ValueError("El título debe tener al menos 10 caracteres")
        
        if len(command.title) > 255:
            raise ValueError("El título no puede exceder 255 caracteres")
        
        # Validar descripción
        if not command.description or len(command.description.strip()) < 50:
            raise ValueError("La descripción debe tener al menos 50 caracteres")
        
        # Validar fechas
        if not self.voting_repository.validate_consultation_dates(command.start_date, command.end_date):
            raise ValueError("Las fechas son inválidas. La fecha de inicio debe ser anterior a la de fin y futura")
        
        # Validar duración mínima (24 horas)
        duration = command.end_date - command.start_date
        if duration < timedelta(hours=24):
            raise ValueError("La consulta debe durar al menos 24 horas")
        
        # Validar duración máxima (30 días)
        if duration > timedelta(days=30):
            raise ValueError("La consulta no puede durar más de 30 días")
        
        # Validar mínimo de votos
        if command.min_votes < 1:
            raise ValueError("El mínimo de votos debe ser al menos 1")
        
        if command.min_votes > 10000:
            raise ValueError("El mínimo de votos no puede exceder 10,000")
    
    def check_voting_eligibility(self, user_id: str, consultation_id: str) -> VotingEligibilityCheck:
        """Verificar elegibilidad completa para votar"""
        return self.voting_repository.check_voting_eligibility(user_id, consultation_id)
    
    def is_user_party_member(self, user_id: str) -> bool:
        """Verificar si un usuario es miembro de partido político"""
        return self.voting_repository.is_user_party_member(user_id)
    
    def can_user_vote_in_consultation(self, user_id: str, consultation_id: str) -> bool:
        """Verificar si un usuario puede votar en una consulta específica"""
        return self.voting_repository.can_user_vote_in_consultation(user_id, consultation_id)
    
    # ============================================
    # MÉTODOS UTILITARIOS
    # ============================================
    
    def get_consultation_summary(self, consultation_id: str) -> Dict[str, Any]:
        """Obtener resumen completo de una consulta"""
        consultation = self.voting_repository.get_consultation(consultation_id)
        if not consultation:
            raise ValueError("La consulta no existe")
        
        # Opciones
        options = self.voting_repository.get_consultation_options(consultation_id)
        
        # Votos
        votes = self.voting_repository.get_consultation_votes(consultation_id)
        
        # Permisos
        permissions = self.voting_repository.get_consultation_permissions(consultation_id)
        
        # Elegibilidad (para usuario actual - si se proporciona)
        
        return {
            "consultation": {
                "id": consultation.id,
                "title": consultation.title,
                "description": consultation.description,
                "status": consultation.status.value,
                "start_date": consultation.start_date.isoformat() if consultation.start_date else None,
                "end_date": consultation.end_date.isoformat() if consultation.end_date else None,
                "min_votes": consultation.min_votes,
                "created_by": consultation.created_by,
                "created_at": consultation.created_at.isoformat() if consultation.created_at else None,
                "is_active": consultation.is_active(),
                "is_finished": consultation.is_finished()
            },
            "options": [
                {
                    "id": option.id,
                    "title": option.title,
                    "description": option.description,
                    "order_index": option.order_index,
                    "votes_count": option.votes_count
                }
                for option in options
            ],
            "voting_stats": {
                "total_votes": len(votes),
                "unique_voters": len(set(v.user_id for v in votes)),
                "total_options": len(options),
                "permissions_granted": len([p for p in permissions if p.can_vote])
            }
        }
