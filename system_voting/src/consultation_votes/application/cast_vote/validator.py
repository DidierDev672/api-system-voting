from system_voting.src.consultation_votes.domain.value_objects.vote_choice import VoteChoice


class VoteValidator:

    @staticmethod
    def validate(
        command,
        member,
        consultation_active,
        already_voted
    ):
        if not VoteChoice.is_valid(command.choice):
            raise ValueError("Opción de voto inválida")

        if not consultation_active:
            raise ValueError("La consulta no está activa")

        if already_voted:
            raise ValueError("El miembro ya votó")