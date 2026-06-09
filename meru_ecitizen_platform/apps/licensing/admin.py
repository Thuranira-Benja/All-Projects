from django.contrib import admin
from .models import BusinessPermit

@admin.register(BusinessPermit)
class BusinessPermitAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'owner', 'status', 'issue_date', 'expiry_date')
    search_fields = ('business_name', 'owner__username', 'ward', 'status')
