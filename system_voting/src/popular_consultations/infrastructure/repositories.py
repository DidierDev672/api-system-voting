from system_voting.src.popular_consultations.application.create_consultation.command import ConsultationRepository
from system_voting.src.popular_consultations.infrastructure.models import PopularConsultationModel


class DjangoConsultationRepository(ConsultationRepository):

    def save(self, consultation):
        PopularConsultationModel.objects.create(
            **consultation.__dict__
        )
        return consultation