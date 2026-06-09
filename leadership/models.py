from django.db import models

class Leadership(models.Model):
    POSITION_CHOICES = (
        ('chairperson', 'Chairperson'),
        ('vice_chair', 'Vice Chairperson'),
        ('secretary', 'Secretary General'),
        ('treasurer', 'Treasurer'),
        ('coordinator', 'Program Coordinator'),
        ('member', 'Executive Member'),
    )
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    title = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='leadership/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'position']
        verbose_name_plural = "Leadership Team"
    
    def __str__(self):
        return f"{self.name} - {self.title}"

class Council(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='council/', blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Executive Council"
    
    def __str__(self):
        return f"{self.name} - {self.role}"
