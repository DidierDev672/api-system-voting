"""
URL Configuration - Screenings
Entry Points
"""

from django.urls import path
from system_voting.src.screening.presentation.controllers.screening_views import (
    ScreeningListCreateView,
    ScreeningDetailView,
)

app_name = "screenings"

urlpatterns = [
    path("", ScreeningListCreateView.as_view(), name="list_create"),
    path("<uuid:screening_id>/", ScreeningDetailView.as_view(), name="detail"),
]
