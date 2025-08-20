# admin.py - Kenyan Version
from django.contrib import admin
from .models import *

@admin.register(SchoolLevel)
class SchoolLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'stream', 'level')
    list_filter = ('level',)

@admin.register(CBCSubject)
class CBCSubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'is_core')
    list_filter = ('level', 'is_core')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('tsc_number', 'name', 'email', 'phone')
    search_fields = ('name', 'tsc_number')
    filter_horizontal = ('subjects',)

@admin.register(MeetingTime)
class MeetingTimeAdmin(admin.ModelAdmin):
    list_display = ('pid', 'day', 'time')
    list_filter = ('day',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'is_special')
    list_filter = ('is_special',)

@admin.register(ClassTimetable)
class ClassTimetableAdmin(admin.ModelAdmin):
    list_display = ('class_level', 'term', 'year', 'is_active')
    list_filter = ('class_level', 'term', 'year', 'is_active')

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('timetable', 'subject', 'teacher', 'meeting_time', 'room')
    list_filter = ('timetable', 'subject', 'teacher')