from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()
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
                questions.append(f"{q}: {data['question']} :- {data['answer']}")
            return '\n'.join(questions)  # Changed from <br> to \n
        return "No security questions"
    security_questions_preview.allow_tags = False  # Changed to False to render newlines properly
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


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('under_process', 'Under Process'),
        ('payment_received', 'Payment Received'),
    ]
    booking = models.ForeignKey(BookingDetail, on_delete=models.CASCADE, related_name='payments', default=None, null=True, blank=True)
    payment_proof = models.FileField(upload_to='payment_proofs/')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='under_process'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"