from system_voting.src.popular_consultations.application.create_consultation.validator import ConsultationValidator
from system_voting.src.popular_consultations.domain.entities.consultation import PopularConsultation


class CreateConsultationHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        ConsultationValidator.validate(command.data)
        consultation = PopularConsultation(**command.data)
        return self.repository.save(consultation)