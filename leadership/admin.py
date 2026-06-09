from django.contrib import admin
from .models import Leadership, Council

@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'position', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('name', 'title', 'bio')

@admin.register(Council)
class CouncilAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role', 'bio')
