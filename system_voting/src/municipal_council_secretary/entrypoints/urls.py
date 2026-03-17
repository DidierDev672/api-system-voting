"""
URL Configuration - Municipal Council Secretary
Entry Points
"""

from django.urls import path
from system_voting.src.municipal_council_secretary.presentation.controllers.municipal_council_secretary_views import (
    MunicipalCouncilSecretaryListCreateView,
    MunicipalCouncilSecretaryDetailView,
)

urlpatterns = [
    path(
        "",
        MunicipalCouncilSecretaryListCreateView.as_view(),
        name="municipal-council-secretary-list-create",
    ),
    path(
        "<str:secretary_id>/",
        MunicipalCouncilSecretaryDetailView.as_view(),
        name="municipal-council-secretary-detail",
    ),
]
