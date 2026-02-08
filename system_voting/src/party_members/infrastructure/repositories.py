from system_voting.src.party_members.domain.ports.member_repository import PartyMemberRepository
from system_voting.src.party_members.infrastructure.models import PartyMemberModel


class DjangoPartyMemberRepository(PartyMemberRepository):

    def save(self, member):
        PartyMemberModel.objects.create(**member.__dict__)
        return member