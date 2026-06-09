from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
