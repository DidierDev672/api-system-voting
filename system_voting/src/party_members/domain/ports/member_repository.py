from abc import ABC, abstractmethod

class PartyMemberRepository(ABC):

    @abstractmethod
    def save(self, member):
        pass