from system_voting.src.party_members.application.register_member.command import RegisterPartyMemberCommand
from system_voting.src.party_members.application.register_member.handler import RegisterPartyMemberHandler
from system_voting.src.party_members.infrastructure.repositories import DjangoPartyMemberRepository

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class RegisterPartyMemberView(APIView):

    def post(self, request):
        command = RegisterPartyMemberCommand(**request.data)
        handler = RegisterPartyMemberHandler(
            DjangoPartyMemberRepository()
        )
        handler.handle(command)

        return Response(
            {"message": "Afiliación registrada correctamente"},
            status=status.HTTP_201_CREATED
        )