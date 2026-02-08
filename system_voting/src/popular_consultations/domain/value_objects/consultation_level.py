class ConsultationLevel:
    NATIONAL = "NATIONAL"
    DEPARTMENT = "DEPARTMENT"
    MUNICIPAL = "MUNICIPAL"

    @classmethod
    def is_valid(cls,value):
        return value in {
            cls.NATIONAL,
            cls.DEPARTMENT,
            cls.MUNICIPAL
        }