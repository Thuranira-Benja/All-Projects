from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
