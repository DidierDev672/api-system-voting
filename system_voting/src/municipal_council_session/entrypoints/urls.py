"""
URL Configuration - Municipal Council Session
Entry Points
"""

from django.urls import path
from system_voting.src.municipal_council_session.presentation.controllers.municipal_council_session_views import (
    MunicipalCouncilSessionListCreateView,
    MunicipalCouncilSessionDetailView,
    SessionMemberView,
    SessionBancadaView,
    SessionAvailableMembersView,
    SessionAvailableBancadasView,
    AllMembersView,
    AllBancadasView,
)

urlpatterns = [
    path(
        "",
        MunicipalCouncilSessionListCreateView.as_view(),
        name="municipal-council-session-list-create",
    ),
    path(
        "members/",
        AllMembersView.as_view(),
        name="all-members",
    ),
    path(
        "bancadas/",
        AllBancadasView.as_view(),
        name="all-bancadas",
    ),
    path(
        "<str:session_id>/",
        MunicipalCouncilSessionDetailView.as_view(),
        name="municipal-council-session-detail",
    ),
    path(
        "<str:session_id>/members/",
        SessionMemberView.as_view(),
        name="session-members",
    ),
    path(
        "<str:session_id>/members/available/",
        SessionAvailableMembersView.as_view(),
        name="session-members-available",
    ),
    path(
        "<str:session_id>/bancadas/",
        SessionBancadaView.as_view(),
        name="session-bancadas",
    ),
    path(
        "<str:session_id>/bancadas/available/",
        SessionAvailableBancadasView.as_view(),
        name="session-bancadas-available",
    ),
]
