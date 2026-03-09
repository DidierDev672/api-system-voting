from django.urls import path
from .views import RegisterPoliticalPartyView, ListPoliticalPartiesView

app_name = 'political_parties'

urlpatterns = [
    path('register/', RegisterPoliticalPartyView.as_view(), name='register_political_party'),
    path('', ListPoliticalPartiesView.as_view(), name='list_political_parties'),
] 