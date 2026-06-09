from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'membership_number', 'is_approved', 'is_staff')
    list_filter = ('is_approved', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'membership_number', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Membership Info', {
            'fields': ('membership_number', 'is_approved', 'approved_at', 'phone_number', 'profile_pic', 'bio', 'department')
        }),
    )
    
    actions = ['approve_members']
    
    def approve_members(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_approved=True, approved_at=timezone.now())
        self.message_user(request, f'{queryset.count()} members approved successfully.')
    approve_members.short_description = "Approve selected members"
