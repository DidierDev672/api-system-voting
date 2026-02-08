class VoteChoice:
    YES = "SI"
    NO = "NO"

    @classmethod
    def is_valid(cls, value):
        return value in { cls.YES, cls.NO }