from abc import ABC, abstractmethod

class PoliticalPartyRepository(ABC):
    @abstractmethod
    def save(self, party):
        pass