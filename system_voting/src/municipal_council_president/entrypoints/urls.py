"""
URL Configuration - Municipal Council President
Entry Points
"""

from django.urls import path
from system_voting.src.municipal_council_president.presentation.controllers.municipal_council_president_views import (
    MunicipalCouncilPresidentListCreateView,
    MunicipalCouncilPresidentDetailView,
)

urlpatterns = [
    path(
        "",
        MunicipalCouncilPresidentListCreateView.as_view(),
        name="municipal-council-president-list-create",
    ),
    path(
        "<str:president_id>/",
        MunicipalCouncilPresidentDetailView.as_view(),
        name="municipal-council-president-detail",
    ),
]
