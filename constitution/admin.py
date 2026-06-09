from django.contrib import admin
from .models import Constitution

@admin.register(Constitution)
class ConstitutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'is_active', 'effective_date', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'content')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'version', 'effective_date', 'is_active')
        }),
        ('Online Reading Content', {
            'fields': ('content',),
            'description': 'This content will be displayed for online reading. You can use the rich text editor to format the constitution.'
        }),
        ('PDF Download', {
            'fields': ('pdf_file',),
            'description': 'Upload a PDF version for users to download.'
        }),
    )
