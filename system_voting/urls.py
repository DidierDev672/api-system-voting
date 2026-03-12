"""
URL configuration for system_voting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/party-members/", include("system_voting.src.party_members.api.urls")),
    path(
        "api/consultation-popular/",
        include("system_voting.src.popular_consultation.entrypoints.urls"),
    ),
    path(
        "api/political-parties/",
        include("system_voting.src.political_parties.api.urls"),
    ),
    path("api/users/", include("system_voting.src.users.api.urls")),
    path("api/vote/", include("system_voting.src.voting.entrypoints.urls")),
]
