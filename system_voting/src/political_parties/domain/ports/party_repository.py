from abc import ABC, abstractmethod

class PoliticalPartyRepository(ABC):
    @abstractmethod
    def save(self, party):
        pass
    
    @abstractmethod
    def get_all(self):
        pass