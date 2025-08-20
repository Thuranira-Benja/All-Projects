from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_of_study = models.CharField(max_length=200)
    skills = models.TextField(help_text="Comma-separated skills (e.g., Python, Accounting, PR)")
    cv = models.FileField(upload_to='cvs/')

class InternshipPost(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField(help_text="Comma-separated skills")
    is_active = models.BooleanField(default=True)

class InternshipApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(InternshipPost, on_delete=models.CASCADE)
    match_score = models.FloatField(default=0.0)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'post')