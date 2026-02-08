class Vote:
    def __init__(self,consultation_id: str,
        member_id: str,
        party_id: str,
        choice: str,
        timestamp: str ):
        self.consultation_id = consultation_id
        self.member_id = member_id
        self.party_id = party_id
        self.choice = choice
        self.timestamp = timestamp