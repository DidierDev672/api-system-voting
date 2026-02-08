class PartyMember:
    def __init__(self, full_name: str,
        document_type: str,
        document_number: str,
        birth_date: str,
        city: str,
        political_party_id: str,
        consent: bool,
        data_authorization: bool,
        affiliation_date: str):
        self.full_name = full_name
        self.document_type = document_type
        self.document_number = document_number
        self.birth_date = birth_date
        self.city = city
        self.political_party_id = political_party_id
        self.consent = consent
        self.data_authorization = data_authorization
        self.affiliation_date = affiliation_date