from django.db import models
from django.conf import settings

class Complaint(models.Model):
    class Category(models.TextChoices):
        HEALTH = 'HEALTH', 'Health'
        ROADS = 'ROADS', 'Roads'
        WATER = 'WATER', 'Water'
        OTHER = 'OTHER', 'Other'

    text = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    confidence_score = models.FloatField(null=True, blank=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)