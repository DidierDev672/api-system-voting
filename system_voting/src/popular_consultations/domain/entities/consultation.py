class PopularConsultation:
    def __init__(
        self,
        title: str,
        question: str,
        justification: str,
        scope: str,
        authority: str,
        proposed_date: str,
        level: str
    ):
        self.title = title
        self.question = question
        self.justification = justification
        self.scope = scope
        self.authority = authority
        self.proposed_date = proposed_date
        self.level = level