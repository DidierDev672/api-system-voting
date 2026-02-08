from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from system_voting.src.consultation_votes.application.cast_vote.command import CastVoteCommand
from system_voting.src.consultation_votes.application.cast_vote.handler import CastVoteHandler
from system_voting.src.consultation_votes.infrastructure.repositories import DjangoVoteRepository
from system_voting.src.party_members.infrastructure.repositories import DjangoPartyMemberRepository
from system_voting.src.popular_consultations.infrastructure.repositories import DjangoConsultationRepository


class CastVoteView(APIView):
    def post(self, request):
        command = CastVoteCommand(
            consultation_id=request.data["consultation_id"],
            member_id=request.data["member_id"],
            choice=request.data["choice"]
        )

        handler = CastVoteHandler(
            DjangoVoteRepository(),
            DjangoPartyMemberRepository(),
            DjangoConsultationRepository()
        )

        handler.handle(command)

        return Response(
            { "message": "Voto registrado correctamente" },
            status=status.HTTP_201_CREATED
        )
