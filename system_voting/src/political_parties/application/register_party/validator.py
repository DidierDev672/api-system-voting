from system_voting.src.political_parties.domain.value_objects.party_type import (
    PartyType,
)


class PoliticalPartyValidator:
    @staticmethod
    def validate(data):
        party_type = PartyType.from_spanish(data["party_type"])

        if not PartyType.is_valid(party_type):
            raise ValueError(
                f"Tipo de organización política no válido. "
                f"Valores permitidos: PARTY, COALITION o MOVEMENT"
            )

        if len(data["acronym"]) > 10:
            raise ValueError("La sigla excede lo permitido")
