from django.urls import path
from .views import RegisterPartyMemberView, ListPartyMembersView, get_member_by_id

app_name = "party_members"

urlpatterns = [
    path("register/", RegisterPartyMemberView.as_view(), name="register_party_member"),
    path("", ListPartyMembersView.as_view(), name="list_party_members"),
    path("<uuid:member_id>/", get_member_by_id, name="get_member_by_id"),
]
