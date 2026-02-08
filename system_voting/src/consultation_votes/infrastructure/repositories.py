from system_voting.src.consultation_votes.domain.ports.vote_repository import VoteRepository
from system_voting.src.consultation_votes.infrastructure.models import VoteModel


class DjangoVoteRepository(VoteRepository):
    def exists(self,  consultation_id, member_id):
        return VoteModel.objects.filter(
            consultation_id=consultation_id,
            member_id=member_id,
        ).exists()

    def save(self, vote):
        VoteModel.objects.create(**vote.__dict__)
        return vote