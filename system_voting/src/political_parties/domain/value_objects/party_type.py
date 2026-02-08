class PartyType:
    PARTY = "PARTY"
    MOVEMENT = "MOVEMENT"

    @classmethod
    def is_valid(cls, value):
        return value in { cls.PARTY, cls.MOVEMENT }