from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    membership_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
    
    def __str__(self):
        return f"{self.username} - {self.membership_number or 'Pending'}"
