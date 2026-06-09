from django.db import models
from django.conf import settings

# Kenyan time slots (8am-3:30pm with breaks)
KENYAN_TIME_SLOTS = (
    ('7:30 - 8:00', 'Morning Assembly'),
    ('8:00 - 8:40', '8:00 - 8:40'),
    ('8:40 - 9:20', '8:40 - 9:20'),
    ('9:20 - 10:00', '9:20 - 10:00'),
    ('10:00 - 10:20', 'Tea Break'),
    ('10:20 - 11:00', '10:20 - 11:00'),
    ('11:00 - 11:40', '11:00 - 11:40'),
    ('11:40 - 12:20', '11:40 - 12:20'),
    ('12:20 - 1:00', '12:20 - 1:00'),
    ('1:00 - 2:00', 'Lunch Break'),
    ('2:00 - 2:40', '2:00 - 2:40'),
    ('2:40 - 3:20', '2:40 - 3:20'),
    ('3:20 - 4:00', 'Games/Remedial'),
)

# Kenyan school days (Monday-Friday)
KENYAN_DAYS = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
)


class SchoolLevel(models.Model):
    LEVEL_CHOICES = (
        ('Pre-Primary', 'Pre-Primary (PP1-PP2)'),
        ('Lower Primary', 'Lower Primary (Grade 1-3)'),
        ('Upper Primary', 'Upper Primary (Grade 4-6)'),
        ('Junior Secondary', 'Junior Secondary (Grade 7-9)'),
        ('Senior Secondary', 'Senior Secondary (Grade 10-12)'),
    )
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.name


class ClassLevel(models.Model):
    GRADE_CHOICES = [
        (f'Grade {i}', f'Grade {i}') for i in range(1, 13)
    ] + [('PP1', 'Pre-Primary 1'), ('PP2', 'Pre-Primary 2')]

    level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=GRADE_CHOICES)
    stream = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return f"{self.name}{self.stream if self.stream else ''}"


class CBCSubject(models.Model):
    SUBJECT_CHOICES = [
        ('Literacy', 'Literacy'),
        ('Kiswahili', 'Kiswahili'),
        ('English', 'English'),
        ('Mathematics', 'Mathematics'),
        ('Environmental', 'Environmental Activities'),
        ('Hygiene', 'Hygiene and Nutrition'),
        ('Religious', 'Religious Education'),
        ('Movement', 'Movement and Creative'),
        ('Art', 'Art and Craft'),
        ('Music', 'Music'),
        ('Science', 'Science and Technology'),
        ('Social', 'Social Studies'),
        ('Agriculture', 'Agriculture'),
        ('Home Science', 'Home Science'),
        ('Business', 'Business Studies'),
        ('Sports', 'Sports and Physical Education'),
        ('Life Skills', 'Life Skills Education'),
    ]

    name = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
    is_core = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    TSC_NUMBER_LENGTH = 10

    tsc_number = models.CharField(max_length=TSC_NUMBER_LENGTH, unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    subjects = models.ManyToManyField(CBCSubject)

    def __str__(self):
        return f"{self.name} ({self.tsc_number})"


class MeetingTime(models.Model):
    pid = models.CharField(max_length=4, primary_key=True)
    time = models.CharField(max_length=50, choices=KENYAN_TIME_SLOTS)
    day = models.CharField(max_length=15, choices=KENYAN_DAYS)

    def __str__(self):
        return f'{self.pid} {self.day} {self.time}'


class Room(models.Model):
    name = models.CharField(max_length=50, default="Room A")
    capacity = models.PositiveIntegerField(default=30)
    is_special = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ClassTimetable(models.Model):
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE)
    term = models.PositiveSmallIntegerField(choices=[(1, 'Term 1'), (2, 'Term 2'), (3, 'Term 3')])
    year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('class_level', 'term', 'year')

    def __str__(self):
        return f"{self.class_level} - Term {self.term} {self.year}"


class TimetableEntry(models.Model):
    timetable = models.ForeignKey(ClassTimetable, on_delete=models.CASCADE)
    subject = models.ForeignKey(CBCSubject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    meeting_time = models.ForeignKey(MeetingTime, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('timetable', 'meeting_time'),
            ('teacher', 'meeting_time'),
            ('room', 'meeting_time'),
        )

    def __str__(self):
        return f"{self.subject} with {self.teacher} at {self.meeting_time}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ttgen_profile'  # Avoids conflict with other apps like 'account'
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
