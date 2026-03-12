"""
URLs para Votación
Vertical Slicing + Hexagonal Architecture
"""

from django.urls import path
from system_voting.src.voting.presentation.controllers.vote_controller import (
    VoteCreateView,
    VoteByConsultationView,
    VoteByMemberView,
)

urlpatterns = [
    # Endpoints de votación
    path("", VoteCreateView.as_view(), name="vote-create"),
    path(
        "consult/<str:id_consult>/",
        VoteByConsultationView.as_view(),
        name="vote-by-consultation",
    ),
    path("member/<str:id_member>/", VoteByMemberView.as_view(), name="vote-by-member"),
]
