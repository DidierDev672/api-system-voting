from django.urls import path
from .views import RegisterPartyMemberView, ListPartyMembersView

app_name = 'party_members'

urlpatterns = [
    path('register/', RegisterPartyMemberView.as_view(), name='register_party_member'),
    path('', ListPartyMembersView.as_view(), name='list_party_members'),
]