from django.urls import path
from .views import RegisterPartyMemberView

app_name = 'party_members'

urlpatterns = [
    path('register/', RegisterPartyMemberView.as_view(), name='register_party_member'),
]