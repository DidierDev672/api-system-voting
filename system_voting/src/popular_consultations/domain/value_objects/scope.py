class Scope:
    GENERAL = "GENERAL"
    TERRITORIAL = "TERRITORIAL"

    @classmethod
    def is_valid(cls, value):
        return value in {cls.GENERAL, cls.TERRITORIAL}