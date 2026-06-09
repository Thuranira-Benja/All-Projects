# forms.py - Kenyan Version
from django import forms
from .models import *

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['tsc_number', 'name', 'phone', 'email', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple,
        }

class CBCSubjectForm(forms.ModelForm):
    class Meta:
        model = CBCSubject
        fields = ['name', 'level', 'is_core']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
        }

class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['level', 'name', 'stream']

class MeetingTimeForm(forms.ModelForm):
    class Meta:
        model = MeetingTime
        fields = ['pid', 'time', 'day']
        widgets = {
            'time': forms.Select(choices=KENYAN_TIME_SLOTS),
            'day': forms.Select(choices=KENYAN_DAYS),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'is_special']

class ClassTimetableForm(forms.ModelForm):
    class Meta:
        model = ClassTimetable
        fields = ['class_level', 'term', 'year']

class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ['subject', 'teacher', 'meeting_time', 'room']