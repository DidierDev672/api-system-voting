from rest_framework.views import APIView
from rest_framework.response import  Response
from rest_framework import status

from system_voting.src.popular_consultations.application.create_consultation.command import CreateConsultationCommand
from system_voting.src.popular_consultations.application.create_consultation.handler import CreateConsultationHandler
from system_voting.src.popular_consultations.infrastructure.repositories import DjangoConsultationRepository


class CreateConsultationView(APIView):
    def post(self, request):
        command = CreateConsultationCommand(**request.data)
        handler = CreateConsultationHandler(
            DjangoConsultationRepository()
        )
        handler.handle(command)

        return Response(
            { "message": "Consulta popular creada (fase administrativa)" },
            status=status.HTTP_200_CREATED,
        )
