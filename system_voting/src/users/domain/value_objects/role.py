class Role:
    ADMIN = "ADMIN"
    USER = "USER"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in [cls.ADMIN, cls.USER]