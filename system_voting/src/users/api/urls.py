from django.urls import path

from system_voting.src.users.api.views import RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
]