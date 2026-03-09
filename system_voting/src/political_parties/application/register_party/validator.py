from system_voting.src.political_parties.domain.value_objects.party_type import PartyType


class PoliticalPartyValidator:

    @staticmethod
    def validate(data):
        if not PartyType.is_valid(data["party_type"]):
            raise ValueError(
                f"Tipo de organización política no válido. "
                f"Valores permitidos: {PartyType.PARTY} o {PartyType.MOVEMENT}"
            )

        if len(data["acronym"]) > 10:
            raise ValueError("La sigla excede lo permitido")