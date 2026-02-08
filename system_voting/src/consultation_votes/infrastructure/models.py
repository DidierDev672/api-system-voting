from django.db import models

class VoteModel(models.Model):
    consultation_id = models.UUIDField()
    member_id = models.UUIDField()
    party_id = models.UUIDField()
    choice = models.CharField(max_length=5)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("consultation_id", "member_id")