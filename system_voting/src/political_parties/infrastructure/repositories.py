from system_voting.src.political_parties.domain.ports.party_repository import PoliticalPartyRepository
from system_voting.src.political_parties.infrastructure.models import PoliticalPartyModel


class DjangoPoliticalPartyRepository(PoliticalPartyRepository):

    def save(self, party):
        PoliticalPartyModel.objects.create(
            **party.__dict__,
        )

        return party