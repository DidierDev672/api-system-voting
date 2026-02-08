from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from system_voting.src.users.application.register_user.command import RegisterUserCommand
from system_voting.src.users.application.register_user.handler import RegisterUserHandler
from system_voting.src.users.infrastructure.repositories import DjangoUserRepository


class RegisterUserView(APIView):
    def post(self, request):
        command = RegisterUserCommand(
            email=request.data['email'],
            password=request.data['password'],
            role=request.data['role']
        )

        handler = RegisterUserHandler(DjangoUserRepository())
        handler.handle(command)

        return Response( {"message": "Usuario registrado correctamente"},
            status=status.HTTP_201_CREATED)