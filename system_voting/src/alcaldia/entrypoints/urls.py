"""
URL Configuration - Alcaldia
Entry Points
"""

from django.urls import path
from system_voting.src.alcaldia.presentation.controllers.alcaldia_views import (
    AlcaldiaListCreateView,
    AlcaldiaDetailView,
)

urlpatterns = [
    path(
        "",
        AlcaldiaListCreateView.as_view(),
        name="alcaldia-list-create",
    ),
    path(
        "<str:alcaldia_id>/",
        AlcaldiaDetailView.as_view(),
        name="alcaldia-detail",
    ),
]
