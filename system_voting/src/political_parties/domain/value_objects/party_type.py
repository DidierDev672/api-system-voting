class PartyType:
    PARTY = "PARTY"
    MOVEMENT = "MOVEMENT"
    COALITION = "COALITION"

    SPANISH_TO_ENUM = {
        "partido": PARTY,
        "coalicion": COALITION,
        "movimiento": MOVEMENT,
    }

    @classmethod
    def is_valid(cls, value):
        return value in {cls.PARTY, cls.MOVEMENT, cls.COALITION}

    @classmethod
    def from_spanish(cls, value: str) -> str:
        return cls.SPANISH_TO_ENUM.get(value.lower(), value.upper())
