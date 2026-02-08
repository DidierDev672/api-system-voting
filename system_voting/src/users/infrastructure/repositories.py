from system_voting.src.users.domain.ports.user_repository import UserRepository
from system_voting.src.users.infrastructure.models import UserModel

class DjangoUserRepository(UserRepository):

    def save(self, user):
        model = UserModel.objects.create_user(
            email=user.email,
            password=user.password,
            role=user.role
        )

        return user