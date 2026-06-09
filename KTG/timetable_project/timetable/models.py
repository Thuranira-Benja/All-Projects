from django.db import models
from django.contrib.auth.models import User

class System(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., 8-4-4, CBC")
    def __str__(self):
        return self.name

class SchoolClass(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text="e.g., Form 1, Grade 5")
    def __str__(self):
        return f"{self.name} ({self.system.name})"
    class Meta:
        unique_together = ('system', 'name')

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    applicable_systems = models.ManyToManyField(System, blank=True)  # NEW: tie subject to system
    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="e.g., +2547XXXXXXX")
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    preferred_classes = models.ManyToManyField(SchoolClass, blank=True)
    max_lessons_per_week = models.PositiveIntegerField(default=25)
    max_lessons_per_day = models.PositiveIntegerField(default=6)
    def __str__(self):
        return self.name

class SubjectAllocation(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lessons_per_week = models.PositiveIntegerField(default=1)
    requires_double_period = models.BooleanField(default=False, help_text="e.g., for practicals like Chemistry")
    def __str__(self):
        return f"{self.subject} for {self.school_class} ({self.lessons_per_week} lessons/week)"
    class Meta:
        unique_together = ('school_class', 'subject')

class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_break = models.BooleanField(default=False)
    def __str__(self):
        break_str = " (Break)" if self.is_break else ""
        return f"{self.day} {self.start_time:%H:%M} - {self.end_time:%H:%M}{break_str}"
    class Meta:
        ordering = ['day', 'start_time']

class Lesson(models.Model):
    subject_allocation = models.ForeignKey(SubjectAllocation, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)  # Denormalized for easier lookups
    def __str__(self):
        return f"Lesson: {self.subject_allocation.subject} for {self.school_class} at {self.time_slot}"
    class Meta:
        unique_together = (('teacher', 'time_slot'), ('school_class', 'time_slot'))

class Student(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    full_name = models.CharField(max_length=200)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.full_name} ({self.school_class})"
