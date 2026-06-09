from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MemberApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    MEMBERSHIP_TYPE = (
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('corporate', 'Corporate'),
    )
    
    # Personal Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Professional Information
    profession = models.CharField(max_length=100)
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(default=0)
    
    # Education
    highest_qualification = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    
    # Membership Details
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPE, default='professional')
    department = models.CharField(max_length=100, blank=True, help_text="Preferred department")
    
    # Why join
    reason_for_joining = models.TextField()
    expectations = models.TextField(blank=True)
    
    # Referral
    referral_source = models.CharField(max_length=200, blank=True)
    referred_by = models.CharField(max_length=100, blank=True)
    
    # Documents
    cv = models.FileField(upload_to='membership/cvs/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='membership/profiles/', blank=True, null=True)
    id_document = models.FileField(upload_to='membership/ids/', blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    membership_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_applications')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.membership_type} ({self.status})"
    
    def save(self, *args, **kwargs):
        if self.status == 'approved' and not self.membership_number:
            import random
            import string
            year = self.approved_at.year if self.approved_at else 2024
            prefix = {'student': 'STU', 'professional': 'PRO', 'corporate': 'COR'}.get(self.membership_type, 'MYP')
            random_digits = ''.join(random.choices(string.digits, k=6))
            self.membership_number = f"{prefix}/{year}/{random_digits}"
        super().save(*args, **kwargs)
