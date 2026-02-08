from abc import ABC, abstractmethod

class VoteRepository(ABC):

    @abstractmethod
    def exists(self, consultation_id, member_id):
        pass
    @abstractmethod
    def save(self, consultation_id, member_id, vote):
        pass