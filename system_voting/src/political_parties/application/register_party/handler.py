from system_voting.src.political_parties.application.register_party.validator import PoliticalPartyValidator
from system_voting.src.political_parties.domain.entities.political_party import PoliticalParty


class RegisterPoliticalPartyHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        PoliticalPartyValidator.validate(command.data)

        party = PoliticalParty(**command.data)
        return self.repository.save(party)