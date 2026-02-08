import datetime

from system_voting.src.consultation_votes.application.cast_vote.validator import VoteValidator
from system_voting.src.consultation_votes.domain.entities.vote import Vote


class CastVoteHandler:

    def __init__(
        self,
        vote_repo,
        member_repo,
        consultation_repo
    ):
        self.vote_repo = vote_repo
        self.member_repo = member_repo
        self.consultation_repo = consultation_repo

    def handle(self, command):
        member = self.member_repo.get_by_id(command.member_id)

        if not member:
            raise ValueError("Miembro no registrado")

        consultation_active = self.consultation_repo.is_active(
            command.consultation_id
        )

        already_voted = self.vote_repo.exists(
            command.consultation_id,
            command.member_id
        )

        VoteValidator.validate(
            command,
            member,
            consultation_active,
            already_voted
        )

        vote = Vote(
            consultation_id=command.consultation_id,
            member_id=member.id,
            party_id=member.political_party_id,
            choice=command.choice,
            timestamp=datetime.utcnow().isoformat()
        )

        return self.vote_repo.save(vote)