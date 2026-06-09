from django.db import models

class Service(models.Model):
    SERVICE_CATEGORIES = [
        ('electrical', 'Electrical & Electronics'),
        ('plumbing', 'Plumbing'),
        ('civil', 'Civil Engineering'),
        ('ict', 'ICT Services'),
        ('mechanical', 'Mechanical'),
        ('automotive', 'Automotive Repair'),
    ]
    
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class", blank=True)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)  # <-- added
    
    def __str__(self):
        return self.title
