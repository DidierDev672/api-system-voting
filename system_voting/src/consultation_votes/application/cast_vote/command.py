class CastVoteCommand:
    def __init__(self, consultation_id, member_id, choice):
        self.consultation_id = consultation_id
        self.member_id = member_id
        self.choice = choice