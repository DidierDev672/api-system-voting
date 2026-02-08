from django.db import models

class PartyMemberModel(models.Model):
    full_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=5)
    document_number = models.CharField(max_length=30)
    birth_date = models.DateField()
    city = models.CharField(max_length=100)
    political_party_id = models.UUIDField()
    consent = models.BooleanField()
    data_authorization = models.BooleanField()
    affiliation_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)