from django.db import models
from django.contrib.auth import get_user_model

# models.py
from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class BookingDetail(models.Model):
    VISA_CHOICES = [
        ('B1B2-Visa', 'B1/B2 Visa'),
        ('H1-H2', 'H1 H4/ L1 L2/ C1D / F1 F2 / J1 J2'),
    ]
    
    LOCATION_CHOICES = [
        ('pan-india', 'Pan India - Biometrics and Interview'),
        ('mumbai', 'Mumbai - Biometrics and Interview'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    visa_type = models.CharField(max_length=50, choices=VISA_CHOICES)
    appointment_location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    travellers = models.PositiveIntegerField(default=1)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # USA Visa Website Access fields
    usavisa_email = models.EmailField(blank=True, null=True)
    usavisa_password = models.CharField(max_length=100, blank=True, null=True)
    security_questions = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.visa_type}"

    class Meta:
        verbose_name = "Booking Detail"
        verbose_name_plural = "Booking Details"


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