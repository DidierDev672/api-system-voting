from django.urls import path, re_path
from ..views import (
    BancadaListCreateView,
    BancadaDetailView,
    BancadaByMiembroView,
    BancadaByPartidoView,
)

urlpatterns = [
    path("", BancadaListCreateView.as_view(), name="bancada-list-create"),
    re_path(
        r"^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$",
        BancadaDetailView.as_view(),
        name="bancada-detail",
    ),
    re_path(
        r"^miembro/(?P<id_miembro>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$",
        BancadaByMiembroView.as_view(),
        name="bancada-by-miembro",
    ),
    re_path(
        r"^partido/(?P<id_partido>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$",
        BancadaByPartidoView.as_view(),
        name="bancada-by-partido",
    ),
]
