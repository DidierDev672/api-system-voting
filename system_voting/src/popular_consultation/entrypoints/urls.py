"""
URLs para Consulta Popular
Configuración de rutas de la API
"""

from django.urls import path
from system_voting.src.popular_consultation.entrypoints.views import (
    ConsultationListCreateView,
    ConsultationDetailView,
    ConsultationPublishView,
    ConsultationCloseView,
)

urlpatterns = [
    # Endpoints principales
    path("", ConsultationListCreateView.as_view(), name="consultation-list-create"),
    path(
        "<str:consultation_id>/",
        ConsultationDetailView.as_view(),
        name="consultation-detail",
    ),
    # Endpoints de estado
    path(
        "<str:consultation_id>/publish/",
        ConsultationPublishView.as_view(),
        name="consultation-publish",
    ),
    path(
        "<str:consultation_id>/close/",
        ConsultationCloseView.as_view(),
        name="consultation-close",
    ),
]
