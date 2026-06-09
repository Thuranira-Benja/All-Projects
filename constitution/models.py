from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Constitution(models.Model):
    title = models.CharField(max_length=200, default="MYP Constitution")
    version = models.CharField(max_length=20, default="1.0")
    content = RichTextUploadingField(blank=True, null=True, help_text="Constitution content for online reading")
    pdf_file = models.FileField(upload_to='constitution/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Constitution"
        ordering = ['-version']
    
    def __str__(self):
        return f"{self.title} v{self.version}"
