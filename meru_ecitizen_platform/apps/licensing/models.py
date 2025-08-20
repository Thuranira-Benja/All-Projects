import uuid
from django.db import models
from django.conf import settings

class BusinessPermit(models.Model):
    class PermitStatus(models.TextChoices):
        PAYMENT_PENDING = 'PAYMENT_PENDING', 'Payment Pending'
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business_name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ward = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PermitStatus.choices, default=PermitStatus.PAYMENT_PENDING)
    receipt_no = models.CharField(max_length=50, blank=True, null=True)
    permit_pdf = models.FileField(upload_to='permits/', blank=True, null=True)
    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.business_name} - {self.status}"
