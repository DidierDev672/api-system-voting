from system_voting.src.party_members.application.register_member.validator import PartyMemberValidator
from system_voting.src.party_members.domain.entities.party_member import PartyMember


class RegisterPartyMemberHandler:

    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        PartyMemberValidator.validate(command.data)
        member = PartyMember(**command.data)
        return self.repository.save(member)