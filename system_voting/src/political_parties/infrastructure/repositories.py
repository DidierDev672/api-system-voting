from system_voting.src.political_parties.domain.ports.party_repository import PoliticalPartyRepository
from system_voting.src.political_parties.infrastructure.models import PoliticalPartyModel
from django.db import IntegrityError

class DjangoPoliticalPartyRepository(PoliticalPartyRepository):

    def save(self, party):
        try:
            PoliticalPartyModel.objects.create(
                **party.__dict__,
            )
            return party
        except IntegrityError as e:
            if "UNIQUE constraint failed: api_politicalpartymodel.name" in str(e):
                raise ValueError(f"Ya existe un partido político con el nombre '{party.name}'")
            elif "UNIQUE constraint failed: api_politicalpartymodel.email" in str(e):
                raise ValueError(f"Ya existe un partido político con el email '{party.email}'")
            else:
                raise ValueError("Error de integridad de datos: " + str(e))
    
    def get_all(self):
        parties = PoliticalPartyModel.objects.all()
        return [
            {
                'id': str(party.id),
                'name': party.name,
                'acronym': party.acronym,
                'party_type': party.party_type,
                'ideology': party.ideology,
                'legal_representative': party.legal_representative,
                'representative_id': party.representative_id,
                'email': party.email,
                'foundation_date': party.foundation_date.isoformat(),
                'created_at': party.created_at.isoformat()
            }
            for party in parties
        ]