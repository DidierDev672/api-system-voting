from rest_framework.views import APIView
from starlette import status

from system_voting.src.political_parties.application.register_party.command import RegisterPoliticalPartyCommand
from system_voting.src.political_parties.application.register_party.handler import RegisterPoliticalPartyHandler
from system_voting.src.political_parties.infrastructure.repositories import DjangoPoliticalPartyRepository


class RegisterPoliticalPartyView(APIView):

    def post(self, request):
        command = RegisterPoliticalPartyCommand(**request.data)
        handler = RegisterPoliticalPartyHandler(
            DjangoPoliticalPartyRepository()
        )

        handler.handle(command)

        return Response({ message: "Solicitud de registro creada" }, status=status.HTTP_201_CREATED)