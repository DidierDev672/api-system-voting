class DocumentType:
    CC = "CC"
    TI = "TI"
    CE = "CE"

    @classmethod
    def is_valid(cls, value):
        return value in {cls.CC, cls.TI, cls.CE}