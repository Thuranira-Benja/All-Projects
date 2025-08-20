from django.contrib import admin
from .models import *

# ✅ Custom Django admin branding
admin.site.site_header = "TGS ADMINISTRATION"
admin.site.site_title = "TGS ADMINISTRATION"
admin.site.index_title = "TGS ADMINISTRATION"

class SubjectAllocationInline(admin.TabularInline):
    model = SubjectAllocation
    extra = 1

@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'system')
    list_filter = ('system',)
    inlines = [SubjectAllocationInline]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_lessons_per_week', 'max_lessons_per_day')
    filter_horizontal = ('subjects', 'preferred_classes')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time', 'is_break')
    list_filter = ('day', 'is_break')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('school_class', 'subject_allocation', 'teacher', 'time_slot')
    list_filter = ('school_class', 'teacher', 'time_slot__day')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# ✅ Register remaining models
admin.site.register(System)
admin.site.register(Subject)
admin.site.register(SubjectAllocation)
admin.site.register(Student)
