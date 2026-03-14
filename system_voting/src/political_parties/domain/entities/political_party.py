class PoliticalParty:
    def __init__(
        self,
        name: str,
        acronym: str,
        party_type: str,
        ideology: str,
        legal_representative: str,
        representative_id: str,
        email: str = None,
        foundation_date: str = None,
        is_active: bool = True,
    ):
        self.name = name
        self.acronym = acronym
        self.party_type = party_type
        self.ideology = ideology
        self.legal_representative = legal_representative
        self.representative_id = representative_id
        self.email = email
        self.foundation_date = foundation_date
        self.is_active = is_active
