"""
URL Configuration - Municipal Council Session
Entry Points
"""

from django.urls import path
from system_voting.src.municipal_council_session.presentation.controllers.municipal_council_session_views import (
    MunicipalCouncilSessionListCreateView,
    MunicipalCouncilSessionDetailView,
)

urlpatterns = [
    path(
        "",
        MunicipalCouncilSessionListCreateView.as_view(),
        name="municipal-council-session-list-create",
    ),
    path(
        "<str:session_id>/",
        MunicipalCouncilSessionDetailView.as_view(),
        name="municipal-council-session-detail",
    ),
]
