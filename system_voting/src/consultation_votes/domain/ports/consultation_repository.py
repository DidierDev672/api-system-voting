from abc import abstractmethod


class ConsultationRepository:
    @abstractmethod
    def is_active(self, consultation_id) -> bool:
        pass