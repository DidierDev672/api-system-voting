from abc import ABC, abstractmethod
from system_voting.src.users.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass