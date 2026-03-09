from system_voting.src.party_members.application.register_member.validator import PartyMemberValidator
from system_voting.src.party_members.application.register_member.command import RegisterPartyMemberCommand
from system_voting.src.party_members.domain.entities.party_member import PartyMember
from datetime import date


class RegisterPartyMemberHandler:

    def __init__(self, repository):
        self.repository = repository

    def handle(self, command):
        # Add affiliation_date if not provided before validation
        data = command.data.copy()
        if 'affiliation_date' not in data:
            data['affiliation_date'] = date.today().isoformat()
        
        # Create a new command with the updated data
        updated_command = RegisterPartyMemberCommand(**data)
        
        PartyMemberValidator.validate(updated_command.data)
        member = PartyMember(**updated_command.data)
        return self.repository.save(member)