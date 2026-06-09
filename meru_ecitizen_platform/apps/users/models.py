from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add extra fields here if needed, e.g., phone number for MPESA
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    # You can add more fields like id_number, ward, etc.

    def __str__(self):
        return self.username