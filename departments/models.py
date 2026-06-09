from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(default="Specialized programmes, mentorship and projects led by member experts.")
    full_description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class (e.g., fa-crown, fa-chart-line)")
    image = models.ImageField(upload_to='departments/', blank=True, null=True)
    leader_name = models.CharField(max_length=100, blank=True)
    leader_title = models.CharField(max_length=100, blank=True)
    leader_image = models.ImageField(upload_to='departments/leaders/', blank=True, null=True)
    member_count = models.IntegerField(default=0)
    project_count = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'departments'
        ordering = ['order']
    
    def __str__(self):
        return self.name
