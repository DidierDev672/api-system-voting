from django.db import models

class PoliticalPartyModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    acronym = models.CharField(max_length=20)
    party_type = models.CharField(max_length=20)
    ideology = models.TextField()
    legal_representative = models.CharField(max_length=255)
    representative_id = models.CharField(max_length=50)
    email = models.EmailField()
    foundation_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)