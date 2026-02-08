from django.db import models

class PopularConsultationModel(models.Model):
    title = models.CharField(max_length=255)
    question = models.TextField()
    justification = models.TextField()
    level = models.CharField(max_length=20)
    scope = models.CharField(max_length=20)
    authority = models.CharField(max_length=255)
    proposed_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)