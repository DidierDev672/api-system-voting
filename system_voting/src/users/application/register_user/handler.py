from system_voting.src.users.domain.entities.user import User
from system_voting.src.users.domain.value_objects.role import Role

class RegisterUserHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        if not Role.is_valid(command.role):
            raise ValueError("Rol no permitido")

        user = User(
            email=command.email,
            password=command.password,
            role=command.role,
        )

        return self.repository.save(user)