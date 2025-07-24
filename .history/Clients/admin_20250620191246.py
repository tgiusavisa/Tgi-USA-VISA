from django.contrib import admin
from .models import BookingDetail, Payment

@admin.register(BookingDetail)
class BookingDetailAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'visa_type', 'appointment_location', 'travellers', 
                   'email', 'mobile_number', 'created_at', 'user', 'usavisa_email')
    list_filter = ('visa_type', 'appointment_location', 'created_at')
    search_fields = ('full_name', 'email', 'mobile_number', 'usavisa_email')
    readonly_fields = ('created_at', 'security_questions_preview')
    
    def security_questions_preview(self, obj):
        if obj.security_questions:
            questions = []
            for q, data in obj.security_questions.items():
                questions.append(f"{q}: {data['question']} - {data['answer']}")
            return '<br>'.join(questions)
        return "No security questions"
    security_questions_preview.allow_tags = True
    security_questions_preview.short_description = 'Security Questions'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'visa_type', 'appointment_location', 'travellers')
        }),
        ('Personal Details', {
            'fields': ('full_name', 'mobile_number', 'email')
        }),
        ('USA Visa Site Access', {
            'fields': ('usavisa_email', 'usavisa_password', 'security_questions_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

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