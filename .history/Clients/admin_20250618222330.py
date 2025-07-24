from django.contrib import admin
from .models import BookingDetail, Payment

@admin.register(BookingDetail)
class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'visa_type', 'appointment_location', 'travellers', 
                   'email', 'mobile_number', 'created_at', 'user')
    list_filter = ('visa_type', 'appointment_location', 'created_at')
    search_fields = ('full_name', 'email', 'mobile_number')
    readonly_fields = ('created_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['mark_as_received']

    def mark_as_received(self, request, queryset):
        queryset.update(status='payment_received')
    mark_as_received.short_description = "Mark selected payments as received"