from abc import ABC, abstractmethod

class ConsultationRepository(ABC):

    @abstractmethod
    def save(self, consultation):
        pass