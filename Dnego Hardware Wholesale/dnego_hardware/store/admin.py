# store/admin.py
import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Category, Product, Order
# ... (Paste the exact same Admin configurations from the first response)
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])
    return response
export_as_csv.short_description = "Export Selected to CSV"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at']
    list_filter = ['category', 'is_available']
    list_editable = ['price', 'stock_quantity', 'is_available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    actions = [export_as_csv]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer_phone', 'quantity', 'total_price', 'status', 'mpesa_receipt_code', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_phone', 'mpesa_receipt_code']
    readonly_fields = ('product', 'quantity', 'total_price', 'customer_phone', 'status', 'checkout_request_id', 'mpesa_receipt_code', 'created_at')
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False