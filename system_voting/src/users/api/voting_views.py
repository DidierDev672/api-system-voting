from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime, timedelta

from ..application.services.voting_service import VotingService
from ..infrastructure.repositories.supabase_voting_repository import SupabaseVotingRepository
from ..domain.entities.voting import (
    CreateConsultationCommand,
    UpdateConsultationCommand,
    CreateVotingOptionCommand,
    VoteCommand,
    GrantVotingPermissionCommand,
    ConsultationStatus
)


class ConsultationListView(APIView):
    """Vista API - Vertical Slicing: Listar Consultas Populares"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def get(self, request):
        """Endpoint GET /api/users/voting/consultations/"""
        try:
            # Parámetros de filtro
            status_filter = request.query_params.get('status')
            limit = int(request.query_params.get('limit', 50))
            
            # Obtener consultas
            consultations = self.voting_service.get_consultations(status_filter, limit)
            
            # Formatear respuesta
            data = []
            for consultation in consultations:
                data.append({
                    "id": consultation.id,
                    "title": consultation.title,
                    "description": consultation.description[:200] + "..." if len(consultation.description) > 200 else consultation.description,
                    "status": consultation.status.value,
                    "start_date": consultation.start_date.isoformat() if consultation.start_date else None,
                    "end_date": consultation.end_date.isoformat() if consultation.end_date else None,
                    "min_votes": consultation.min_votes,
                    "total_votes": consultation.total_votes,
                    "total_options": consultation.total_options,
                    "is_active": consultation.is_active(),
                    "created_at": consultation.created_at.isoformat() if consultation.created_at else None
                })
            
            return Response({
                "success": True,
                "message": "Consultas obtenidas exitosamente",
                "data": data,
                "count": len(data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al obtener consultas: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultationDetailView(APIView):
    """Vista API - Vertical Slicing: Detalle de Consulta Popular"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def get(self, request, consultation_id):
        """Endpoint GET /api/users/voting/consultations/<uuid>/"""
        try:
            # Obtener resumen completo
            summary = self.voting_service.get_consultation_summary(consultation_id)
            
            return Response({
                "success": True,
                "message": "Consulta obtenida exitosamente",
                "data": summary
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al obtener consulta: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateConsultationView(APIView):
    """Vista API - Vertical Slicing: Crear Consulta Popular"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def post(self, request):
        """Endpoint POST /api/users/voting/consultations/"""
        try:
            data = request.data
            
            # Validaciones básicas
            required_fields = ["title", "description", "start_date", "end_date"]
            for field in required_fields:
                if not data.get(field):
                    return Response({
                        "success": False,
                        "error": f"El campo {field} es obligatorio"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Parsear fechas
            try:
                start_date = datetime.fromisoformat(data["start_date"].replace('Z', '+00:00'))
                end_date = datetime.fromisoformat(data["end_date"].replace('Z', '+00:00'))
            except ValueError:
                return Response({
                    "success": False,
                    "error": "Formato de fecha inválido. Use ISO 8601"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear comando
            command = CreateConsultationCommand(
                title=data["title"].strip(),
                description=data["description"].strip(),
                start_date=start_date,
                end_date=end_date,
                min_votes=data.get("min_votes", 1),
                created_by=str(request.user.id) if hasattr(request, 'user') and request.user else "demo-user"
            )
            
            # Crear consulta
            consultation = self.voting_service.create_consultation(command)
            
            return Response({
                "success": True,
                "message": "Consulta creada exitosamente",
                "data": {
                    "id": consultation.id,
                    "title": consultation.title,
                    "status": consultation.status.value,
                    "start_date": consultation.start_date.isoformat(),
                    "end_date": consultation.end_date.isoformat(),
                    "created_at": consultation.created_at.isoformat() if consultation.created_at else None
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al crear consulta: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VoteView(APIView):
    """Vista API - Vertical Slicing: Votar en Consulta Popular"""
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def post(self, request, consultation_id):
        """Endpoint POST /api/users/voting/consultations/<uuid>/vote/"""
        try:
            data = request.data
            
            if not data.get("option_id"):
                return Response({
                    "success": False,
                    "error": "El option_id es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar elegibilidad primero
            user_id = str(request.user.id) if hasattr(request, 'user') and request.user else "demo-user-1"
            eligibility = self.voting_service.check_voting_eligibility(user_id, consultation_id)
            
            if not eligibility.is_eligible:
                return Response({
                    "success": False,
                    "error": "No puede votar",
                    "reasons": eligibility.reasons
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Crear comando de voto
            command = VoteCommand(
                consultation_id=consultation_id,
                option_id=data["option_id"],
                user_id=user_id,
                party_member_id=None  # Se podría obtener del repositorio de party_members
            )
            
            # Registrar voto
            vote = self.voting_service.cast_vote(command)
            
            return Response({
                "success": True,
                "message": "Voto registrado exitosamente",
                "data": {
                    "vote_id": vote.id,
                    "consultation_id": vote.consultation_id,
                    "option_id": vote.option_id,
                    "voted_at": vote.voted_at.isoformat()
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al registrar voto: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VotingEligibilityView(APIView):
    """Vista API - Vertical Slicing: Verificar Elegibilidad para Votar"""
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def get(self, request, consultation_id):
        """Endpoint GET /api/users/voting/consultations/<uuid>/eligibility/"""
        try:
            user_id = str(request.user.id) if hasattr(request, 'user') and request.user else "demo-user-1"
            
            # Verificar elegibilidad
            eligibility = self.voting_service.check_voting_eligibility(user_id, consultation_id)
            
            # Verificar si ya votó
            has_voted = self.voting_service.has_user_voted(user_id, consultation_id)
            
            return Response({
                "success": True,
                "message": "Elegibilidad verificada",
                "data": {
                    "user_id": eligibility.user_id,
                    "consultation_id": eligibility.consultation_id,
                    "is_eligible": eligibility.is_eligible,
                    "has_voted": has_voted,
                    "reasons": eligibility.reasons,
                    "is_party_member": eligibility.is_party_member(),
                    "has_permission": eligibility.has_permission()
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al verificar elegibilidad: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultationResultsView(APIView):
    """Vista API - Vertical Slicing: Resultados de Consulta Popular"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def get(self, request, consultation_id):
        """Endpoint GET /api/users/voting/consultations/<uuid>/results/"""
        try:
            # Obtener resultados
            results = self.voting_service.get_consultation_results(consultation_id)
            
            # Obtener información de la consulta
            consultation = self.voting_service.get_consultation(consultation_id)
            if not consultation:
                return Response({
                    "success": False,
                    "error": "La consulta no existe"
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "success": True,
                "message": "Resultados obtenidos exitosamente",
                "data": {
                    "consultation_id": results.consultation_id,
                    "consultation_title": results.consultation_title,
                    "total_votes": results.total_votes,
                    "status": consultation.status.value,
                    "is_finished": consultation.is_finished(),
                    "options": results.options,
                    "winner": results.get_winner()
                }
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al obtener resultados: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VotingPermissionView(APIView):
    """Vista API - Vertical Slicing: Gestionar Permisos de Votación"""
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def post(self, request, consultation_id):
        """Endpoint POST /api/users/voting/consultations/<uuid>/permissions/"""
        try:
            data = request.data
            
            if not data.get("user_id"):
                return Response({
                    "success": False,
                    "error": "El user_id es obligatorio"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear comando
            command = GrantVotingPermissionCommand(
                user_id=data["user_id"],
                consultation_id=consultation_id,
                can_vote=data.get("can_vote", True),
                granted_by=str(request.user.id) if hasattr(request, 'user') and request.user else "admin-user"
            )
            
            # Otorgar permiso
            permission = self.voting_service.grant_voting_permission(command)
            
            return Response({
                "success": True,
                "message": "Permiso otorgado exitosamente",
                "data": {
                    "permission_id": permission.id,
                    "user_id": permission.user_id,
                    "consultation_id": permission.consultation_id,
                    "can_vote": permission.can_vote,
                    "granted_at": permission.granted_at.isoformat() if permission.granted_at else None
                }
            }, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al otorgar permiso: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, consultation_id, user_id):
        """Endpoint DELETE /api/users/voting/consultations/<uuid>/permissions/<uuid>/"""
        try:
            # Revocar permiso
            success = self.voting_service.revoke_voting_permission(user_id, consultation_id)
            
            if success:
                return Response({
                    "success": True,
                    "message": "Permiso revocado exitosamente"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "error": "No se pudo revocar el permiso"
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except ValueError as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al revocar permiso: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VotingDashboardView(APIView):
    """Vista API - Vertical Slicing: Dashboard de Votación"""
    permission_classes = [AllowAny]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def get(self, request):
        """Endpoint GET /api/users/voting/dashboard/"""
        try:
            # Obtener datos del dashboard
            dashboard_data = self.voting_service.get_dashboard_data()
            
            return Response({
                "success": True,
                "message": "Dashboard obtenido exitosamente",
                "data": dashboard_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al obtener dashboard: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserVotingHistoryView(APIView):
    """Vista API - Vertical Slicing: Historial de Votos del Usuario"""
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        super().__init__()
        voting_repository = SupabaseVotingRepository()
        self.voting_service = VotingService(voting_repository)
    
    def get(self, request):
        """Endpoint GET /api/users/voting/history/"""
        try:
            user_id = str(request.user.id) if hasattr(request, 'user') and request.user else "demo-user-1"
            
            # Obtener historial de votos
            votes = self.voting_service.get_user_votes(user_id)
            
            # Formatear respuesta
            data = []
            for vote in votes:
                # Obtener información de la consulta y opción
                consultation = self.voting_service.get_consultation(vote.consultation_id)
                options = self.voting_service.voting_repository.get_consultation_options(vote.consultation_id)
                option = next((o for o in options if o.id == vote.option_id), None)
                
                data.append({
                    "vote_id": vote.id,
                    "consultation_id": vote.consultation_id,
                    "consultation_title": consultation.title if consultation else "Consulta no encontrada",
                    "option_id": vote.option_id,
                    "option_title": option.title if option else "Opción no encontrada",
                    "voted_at": vote.voted_at.isoformat()
                })
            
            return Response({
                "success": True,
                "message": "Historial de votos obtenido exitosamente",
                "data": data,
                "count": len(data)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "success": False,
                "error": f"Error al obtener historial: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
