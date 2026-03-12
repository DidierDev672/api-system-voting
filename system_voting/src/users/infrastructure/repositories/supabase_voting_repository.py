from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

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


class SupabaseVotingRepository(VotingRepositoryPort):
    """Implementación del repositorio de votación con Supabase"""
    
    def __init__(self):
        from django.conf import settings
        self.supabase_url = getattr(settings, 'SUPABASE_URL', 'https://your-project.supabase.co')
        self.supabase_key = getattr(settings, 'SUPABASE_ANON_KEY', 'your-anon-key')
        
        # Modo demo para pruebas sin Supabase
        self.demo_mode = self.supabase_url == 'https://your-project.supabase.co'
        
        if not self.demo_mode:
            from supabase import create_client
            self.supabase = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            # Datos de demo
            self._demo_consultations = {}
            self._demo_options = {}
            self._demo_votes = {}
            self._demo_permissions = {}
    
    # ============================================
    # CONSULTAS POPULARES
    # ============================================
    
    def create_consultation(self, command: CreateConsultationCommand) -> PopularConsultation:
        """Crear una nueva consulta popular"""
        if self.demo_mode:
            consultation_id = str(uuid.uuid4())
            consultation = PopularConsultation(
                id=consultation_id,
                title=command.title,
                description=command.description,
                start_date=command.start_date,
                end_date=command.end_date,
                min_votes=command.min_votes,
                created_by=command.created_by,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self._demo_consultations[consultation_id] = consultation
            return consultation
        
        data = {
            'title': command.title,
            'description': command.description,
            'start_date': command.start_date.isoformat(),
            'end_date': command.end_date.isoformat(),
            'min_votes': command.min_votes,
            'created_by': command.created_by if command.created_by != 'demo-user' else None
        }
        
        result = self.supabase.table('popular_consultations').insert(data).execute()
        return self._map_to_consultation(result.data[0])
    
    def get_consultation(self, consultation_id: str) -> Optional[PopularConsultation]:
        """Obtener una consulta por ID"""
        if self.demo_mode:
            consultation = self._demo_consultations.get(consultation_id)
            if consultation:
                consultation.options = self.get_consultation_options(consultation_id)
                consultation.total_votes = len([v for v in self._demo_votes.values() if v.consultation_id == consultation_id])
                consultation.total_options = len(consultation.options)
            return consultation
        
        result = self.supabase.table('popular_consultations').select('*').eq('id', consultation_id).execute()
        if not result.data:
            return None
        
        consultation = self._map_to_consultation(result.data[0])
        consultation.options = self.get_consultation_options(consultation_id)
        consultation.total_votes = self.get_vote_count(consultation_id)
        consultation.total_options = len(consultation.options)
        
        return consultation
    
    def get_consultations(self, status: Optional[str] = None, limit: int = 50) -> List[PopularConsultation]:
        """Obtener lista de consultas populares"""
        if self.demo_mode:
            consultations = list(self._demo_consultations.values())
            if status:
                consultations = [c for c in consultations if c.status.value == status]
            return consultations[:limit]
        
        query = self.supabase.table('popular_consultations').select('*')
        if status:
            query = query.eq('status', status)
        
        result = query.limit(limit).execute()
        consultations = []
        
        for item in result.data:
            consultation = self._map_to_consultation(item)
            consultation.options = self.get_consultation_options(consultation.id)
            consultation.total_votes = self.get_vote_count(consultation.id)
            consultation.total_options = len(consultation.options)
            consultations.append(consultation)
        
        return consultations
    
    def update_consultation(self, command: UpdateConsultationCommand) -> Optional[PopularConsultation]:
        """Actualizar una consulta popular"""
        if self.demo_mode:
            consultation = self._demo_consultations.get(command.id)
            if not consultation:
                return None
            
            if command.title:
                consultation.title = command.title
            if command.description:
                consultation.description = command.description
            if command.start_date:
                consultation.start_date = command.start_date
            if command.end_date:
                consultation.end_date = command.end_date
            if command.status:
                consultation.status = command.status
            if command.min_votes:
                consultation.min_votes = command.min_votes
            
            consultation.updated_at = datetime.now()
            return consultation
        
        data = {}
        if command.title:
            data['title'] = command.title
        if command.description:
            data['description'] = command.description
        if command.start_date:
            data['start_date'] = command.start_date.isoformat()
        if command.end_date:
            data['end_date'] = command.end_date.isoformat()
        if command.status:
            data['status'] = command.status.value
        if command.min_votes:
            data['min_votes'] = command.min_votes
        
        result = self.supabase.table('popular_consultations').update(data).eq('id', command.id).execute()
        if not result.data:
            return None
        
        return self._map_to_consultation(result.data[0])
    
    def delete_consultation(self, consultation_id: str) -> bool:
        """Eliminar una consulta popular"""
        if self.demo_mode:
            return self._demo_consultations.pop(consultation_id, None) is not None
        
        result = self.supabase.table('popular_consultations').delete().eq('id', consultation_id).execute()
        return len(result.data) > 0
    
    def get_active_consultations(self) -> List[PopularConsultation]:
        """Obtener consultas activas"""
        if self.demo_mode:
            now = datetime.now()
            return [
                c for c in self._demo_consultations.values()
                if c.status == ConsultationStatus.ACTIVE and c.start_date <= now and c.end_date > now
            ]
        
        result = self.supabase.table('active_consultations').select('*').execute()
        consultations = []
        
        for item in result.data:
            consultation = self._map_to_consultation(item)
            consultation.options = self.get_consultation_options(consultation.id)
            consultation.total_votes = self.get_vote_count(consultation.id)
            consultation.total_options = len(consultation.options)
            consultations.append(consultation)
        
        return consultations
    
    # ============================================
    # OPCIONES DE VOTACIÓN
    # ============================================
    
    def create_voting_option(self, command: CreateVotingOptionCommand) -> VotingOption:
        """Crear una opción de votación"""
        if self.demo_mode:
            option_id = str(uuid.uuid4())
            option = VotingOption(
                id=option_id,
                consultation_id=command.consultation_id,
                title=command.title,
                description=command.description,
                order_index=command.order_index,
                created_at=datetime.now()
            )
            self._demo_options[option_id] = option
            return option
        
        data = {
            'consultation_id': command.consultation_id,
            'title': command.title,
            'description': command.description,
            'order_index': command.order_index
        }
        
        result = self.supabase.table('voting_options').insert(data).execute()
        return self._map_to_voting_option(result.data[0])
    
    def get_consultation_options(self, consultation_id: str) -> List[VotingOption]:
        """Obtener opciones de una consulta"""
        if self.demo_mode:
            return [opt for opt in self._demo_options.values() if opt.consultation_id == consultation_id]
        
        result = self.supabase.table('voting_options').select('*').eq('consultation_id', consultation_id).order('order_index').execute()
        return [self._map_to_voting_option(item) for item in result.data]
    
    def update_voting_option(self, option_id: str, data: Dict[str, Any]) -> Optional[VotingOption]:
        """Actualizar una opción de votación"""
        if self.demo_mode:
            option = self._demo_options.get(option_id)
            if not option:
                return None
            
            if 'title' in data:
                option.title = data['title']
            if 'description' in data:
                option.description = data['description']
            if 'order_index' in data:
                option.order_index = data['order_index']
            
            return option
        
        result = self.supabase.table('voting_options').update(data).eq('id', option_id).execute()
        if not result.data:
            return None
        
        return self._map_to_voting_option(result.data[0])
    
    def delete_voting_option(self, option_id: str) -> bool:
        """Eliminar una opción de votación"""
        if self.demo_mode:
            return self._demo_options.pop(option_id, None) is not None
        
        result = self.supabase.table('voting_options').delete().eq('id', option_id).execute()
        return len(result.data) > 0
    
    # ============================================
    # VOTOS
    # ============================================
    
    def cast_vote(self, command: VoteCommand) -> Vote:
        """Registrar un voto"""
        if self.demo_mode:
            vote_id = str(uuid.uuid4())
            vote = Vote(
                id=vote_id,
                consultation_id=command.consultation_id,
                option_id=command.option_id,
                user_id=command.user_id,
                party_member_id=command.party_member_id,
                voted_at=datetime.now()
            )
            self._demo_votes[vote_id] = vote
            
            # Actualizar contador de votos en la opción
            for option in self._demo_options.values():
                if option.id == command.option_id:
                    option.votes_count += 1
                    break
            
            return vote
        
        data = {
            'consultation_id': command.consultation_id,
            'option_id': command.option_id,
            'user_id': command.user_id,
            'party_member_id': command.party_member_id
        }
        
        result = self.supabase.table('votes').insert(data).execute()
        return self._map_to_vote(result.data[0])
    
    def get_user_votes(self, user_id: str) -> List[Vote]:
        """Obtener votos de un usuario"""
        if self.demo_mode:
            return [v for v in self._demo_votes.values() if v.user_id == user_id]
        
        result = self.supabase.table('votes').select('*').eq('user_id', user_id).execute()
        return [self._map_to_vote(item) for item in result.data]
    
    def get_consultation_votes(self, consultation_id: str) -> List[Vote]:
        """Obtener votos de una consulta"""
        if self.demo_mode:
            return [v for v in self._demo_votes.values() if v.consultation_id == consultation_id]
        
        result = self.supabase.table('votes').select('*').eq('consultation_id', consultation_id).execute()
        return [self._map_to_vote(item) for item in result.data]
    
    def has_user_voted(self, user_id: str, consultation_id: str) -> bool:
        """Verificar si un usuario ya votó en una consulta"""
        if self.demo_mode:
            return any(v.user_id == user_id and v.consultation_id == consultation_id for v in self._demo_votes.values())
        
        result = self.supabase.table('votes').select('id').eq('user_id', user_id).eq('consultation_id', consultation_id).execute()
        return len(result.data) > 0
    
    def get_vote_count(self, consultation_id: str, option_id: str = None) -> int:
        """Obtener conteo de votos"""
        if self.demo_mode:
            if option_id:
                return len([v for v in self._demo_votes.values() if v.consultation_id == consultation_id and v.option_id == option_id])
            else:
                return len([v for v in self._demo_votes.values() if v.consultation_id == consultation_id])
        
        if option_id:
            result = self.supabase.table('votes').select('id').eq('consultation_id', consultation_id).eq('option_id', option_id).execute()
        else:
            result = self.supabase.table('votes').select('id').eq('consultation_id', consultation_id).execute()
        
        return len(result.data)
    
    # ============================================
    # PERMISOS DE VOTACIÓN
    # ============================================
    
    def grant_voting_permission(self, command: GrantVotingPermissionCommand) -> VotingPermission:
        """Otorgar permiso de votación"""
        if self.demo_mode:
            permission_id = str(uuid.uuid4())
            permission = VotingPermission(
                id=permission_id,
                user_id=command.user_id,
                consultation_id=command.consultation_id,
                can_vote=command.can_vote,
                granted_by=command.granted_by,
                granted_at=datetime.now()
            )
            self._demo_permissions[f"{command.user_id}_{command.consultation_id}"] = permission
            return permission
        
        data = {
            'user_id': command.user_id,
            'consultation_id': command.consultation_id,
            'can_vote': command.can_vote,
            'granted_by': command.granted_by
        }
        
        result = self.supabase.table('voting_permissions').insert(data).execute()
        return self._map_to_voting_permission(result.data[0])
    
    def revoke_voting_permission(self, user_id: str, consultation_id: str) -> bool:
        """Revocar permiso de votación"""
        if self.demo_mode:
            return self._demo_permissions.pop(f"{user_id}_{consultation_id}", None) is not None
        
        result = self.supabase.table('voting_permissions').delete().eq('user_id', user_id).eq('consultation_id', consultation_id).execute()
        return len(result.data) > 0
    
    def get_user_voting_permission(self, user_id: str, consultation_id: str) -> Optional[VotingPermission]:
        """Obtener permiso de votación de un usuario"""
        if self.demo_mode:
            return self._demo_permissions.get(f"{user_id}_{consultation_id}")
        
        result = self.supabase.table('voting_permissions').select('*').eq('user_id', user_id).eq('consultation_id', consultation_id).execute()
        if not result.data:
            return None
        
        return self._map_to_voting_permission(result.data[0])
    
    def get_consultation_permissions(self, consultation_id: str) -> List[VotingPermission]:
        """Obtener permisos de una consulta"""
        if self.demo_mode:
            return [p for p in self._demo_permissions.values() if p.consultation_id == consultation_id]
        
        result = self.supabase.table('voting_permissions').select('*').eq('consultation_id', consultation_id).execute()
        return [self._map_to_voting_permission(item) for item in result.data]
    
    def check_voting_eligibility(self, user_id: str, consultation_id: str) -> VotingEligibilityCheck:
        """Verificar elegibilidad para votar"""
        check = VotingEligibilityCheck(user_id=user_id, consultation_id=consultation_id, is_eligible=True)
        
        # Verificar si ya votó
        if self.has_user_voted(user_id, consultation_id):
            check.add_reason("Ya ha votado en esta consulta")
        
        # Verificar si es miembro de partido
        if not self.is_user_party_member(user_id):
            check.add_reason("No es miembro de partido político")
        
        # Verificar si tiene permiso
        permission = self.get_user_voting_permission(user_id, consultation_id)
        if not permission or not permission.can_vote:
            check.add_reason("No tiene permiso de votación")
        
        # Verificar si la consulta está activa
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            check.add_reason("La consulta no existe")
        elif not consultation.can_vote():
            check.add_reason("La consulta no está activa para votación")
        
        return check
    
    # ============================================
    # RESULTADOS Y ESTADÍSTICAS
    # ============================================
    
    def get_consultation_results(self, consultation_id: str) -> VotingResults:
        """Obtener resultados de una consulta"""
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            raise ValueError("Consulta no encontrada")
        
        results = VotingResults(
            consultation_id=consultation_id,
            consultation_title=consultation.title,
            total_votes=self.get_vote_count(consultation_id)
        )
        
        options = self.get_consultation_options(consultation_id)
        for option in options:
            votes = self.get_vote_count(consultation_id, option.id)
            percentage = (votes / results.total_votes * 100) if results.total_votes > 0 else 0
            results.add_option_result(option.id, option.title, votes, percentage)
        
        return results
    
    def get_eligible_voters(self, consultation_id: str) -> List[EligibleVoter]:
        """Obtener votantes elegibles para una consulta"""
        if self.demo_mode:
            # Datos de demo para votantes elegibles
            return [
                EligibleVoter(
                    user_id="demo-user-1",
                    full_name="Usuario Demo 1",
                    email="demo1@example.com",
                    party_member_id="party-member-1",
                    party_id="party-1",
                    party_name="Partido Demo",
                    consultation_id=consultation_id,
                    can_vote=True
                )
            ]
        
        result = self.supabase.table('eligible_voters').select('*').eq('consultation_id', consultation_id).execute()
        return [self._map_to_eligible_voter(item) for item in result.data]
    
    def get_voting_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas generales de votación"""
        if self.demo_mode:
            return {
                "total_consultations": len(self._demo_consultations),
                "active_consultations": len([c for c in self._demo_consultations.values() if c.status == ConsultationStatus.ACTIVE]),
                "total_votes": len(self._demo_votes),
                "total_voters": len(set(v.user_id for v in self._demo_votes.values()))
            }
        
        # Usar RPC para estadísticas en Supabase
        stats = {}
        
        # Consultas totales
        result = self.supabase.table('popular_consultations').select('id', count='exact').execute()
        stats["total_consultations"] = result.count or 0
        
        # Consultas activas
        result = self.supabase.table('popular_consultations').select('id', count='exact').eq('status', 'ACTIVE').execute()
        stats["active_consultations"] = result.count or 0
        
        # Votos totales
        result = self.supabase.table('votes').select('id', count='exact').execute()
        stats["total_votes"] = result.count or 0
        
        # Votantes únicos
        result = self.supabase.rpc('get_unique_voters_count').execute()
        stats["total_voters"] = result.data or 0
        
        return stats
    
    # ============================================
    # VALIDACIONES DE NEGOCIO
    # ============================================
    
    def validate_consultation_dates(self, start_date: datetime, end_date: datetime) -> bool:
        """Validar fechas de consulta"""
        from datetime import timezone
        now = datetime.now(timezone.utc)
        return start_date < end_date and start_date > now
    
    def can_user_vote_in_consultation(self, user_id: str, consultation_id: str) -> bool:
        """Verificar si un usuario puede votar en una consulta"""
        eligibility = self.check_voting_eligibility(user_id, consultation_id)
        return eligibility.is_eligible
    
    def is_user_party_member(self, user_id: str) -> bool:
        """Verificar si un usuario es miembro de partido político"""
        if self.demo_mode:
            # En modo demo, asumimos que algunos usuarios son miembros
            return user_id.startswith("demo-user")
        
        result = self.supabase.table('party_members').select('id').eq('user_id', user_id).eq('is_active', True).execute()
        return len(result.data) > 0
    
    # ============================================
    # MÉTODOS DE MAPEO
    # ============================================
    
    def _map_to_consultation(self, data: Dict[str, Any]) -> PopularConsultation:
        """Mapear datos a entidad PopularConsultation"""
        return PopularConsultation(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            start_date=datetime.fromisoformat(data.get('start_date', '')) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data.get('end_date', '')) if data.get('end_date') else None,
            status=ConsultationStatus(data.get('status', 'ACTIVE')),
            min_votes=data.get('min_votes', 1),
            created_by=data.get('created_by'),
            created_at=datetime.fromisoformat(data.get('created_at', '')) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data.get('updated_at', '')) if data.get('updated_at') else None
        )
    
    def _map_to_voting_option(self, data: Dict[str, Any]) -> VotingOption:
        """Mapear datos a entidad VotingOption"""
        return VotingOption(
            id=data.get('id'),
            consultation_id=data.get('consultation_id', ''),
            title=data.get('title', ''),
            description=data.get('description'),
            order_index=data.get('order_index', 0),
            votes_count=data.get('votes_count', 0),
            created_at=datetime.fromisoformat(data.get('created_at', '')) if data.get('created_at') else None
        )
    
    def _map_to_vote(self, data: Dict[str, Any]) -> Vote:
        """Mapear datos a entidad Vote"""
        return Vote(
            id=data.get('id'),
            consultation_id=data.get('consultation_id', ''),
            option_id=data.get('option_id', ''),
            user_id=data.get('user_id', ''),
            party_member_id=data.get('party_member_id'),
            voted_at=datetime.fromisoformat(data.get('voted_at', '')) if data.get('voted_at') else None
        )
    
    def _map_to_voting_permission(self, data: Dict[str, Any]) -> VotingPermission:
        """Mapear datos a entidad VotingPermission"""
        return VotingPermission(
            id=data.get('id'),
            user_id=data.get('user_id', ''),
            consultation_id=data.get('consultation_id', ''),
            can_vote=data.get('can_vote', False),
            granted_by=data.get('granted_by'),
            granted_at=datetime.fromisoformat(data.get('granted_at', '')) if data.get('granted_at') else None
        )
    
    def _map_to_eligible_voter(self, data: Dict[str, Any]) -> EligibleVoter:
        """Mapear datos a entidad EligibleVoter"""
        return EligibleVoter(
            user_id=data.get('user_id', ''),
            full_name=data.get('full_name', ''),
            email=data.get('email', ''),
            party_member_id=data.get('party_member_id'),
            party_id=data.get('party_id'),
            party_name=data.get('party_name'),
            consultation_id=data.get('consultation_id'),
            can_vote=data.get('can_vote', True)
        )
