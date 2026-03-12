from django.urls import path
from .voting_views import (
    ConsultationListView,
    ConsultationDetailView,
    CreateConsultationView,
    VoteView,
    VotingEligibilityView,
    ConsultationResultsView,
    VotingPermissionView,
    VotingDashboardView,
    UserVotingHistoryView
)

app_name = 'voting'

urlpatterns = [
    # ============================================
    # ENDPOINTS PRINCIPALES DE VOTACIÓN
    # ============================================
    
    # Dashboard y estadísticas
    path('dashboard/', VotingDashboardView.as_view(), name='voting_dashboard'),
    
    # Consultas populares
    path('consultations/', ConsultationListView.as_view(), name='consultation_list'),
    path('consultations/create/', CreateConsultationView.as_view(), name='create_consultation'),
    path('consultations/<uuid:consultation_id>/', ConsultationDetailView.as_view(), name='consultation_detail'),
    
    # Votación
    path('consultations/<uuid:consultation_id>/vote/', VoteView.as_view(), name='cast_vote'),
    path('consultations/<uuid:consultation_id>/eligibility/', VotingEligibilityView.as_view(), name='voting_eligibility'),
    path('consultations/<uuid:consultation_id>/results/', ConsultationResultsView.as_view(), name='consultation_results'),
    
    # Permisos de votación
    path('consultations/<uuid:consultation_id>/permissions/', VotingPermissionView.as_view(), name='voting_permissions'),
    path('consultations/<uuid:consultation_id>/permissions/<uuid:user_id>/', VotingPermissionView.as_view(), name='revoke_voting_permission'),
    
    # Historial de usuario
    path('history/', UserVotingHistoryView.as_view(), name='user_voting_history'),
]
