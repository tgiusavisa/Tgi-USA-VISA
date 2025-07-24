from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class BookingDetail(models.Model):
    VISA_CHOICES = [
        ('B1B2-Visa', 'B1B2 Visa'),
        ('B1B2-Visa Dropbox', 'B1B2 Visa Dropbox'),
        ('C1d-Visa', 'C1d- fresh or Dropbox'),
        ('H1b/H4-Visa', 'H1b/H4- Fresh or Dropbox'),
        ('F1/F2-Visa', 'F1/F2- fresh or dropbox'),
        ('L1/L2-Visa', 'L1/L2- Fresh or Dropbox'),
        ('Blanket-L1-Visa', 'Blanket L1 Visa'),
        ('Blanket-L2-Visa-Drop-visa', 'Blanket L2 Visa Drop/Fresh'),
        ('Immigration-Visa', 'Immigration Visa Any category'),
    ]
    Service_CHOICES = [
        ('Only-Slot-Booking', 'Only Slot Booking'),
        ('Only-Normal-Process', 'Only Normal Process'),
        ('Express-Dates', 'Express Dates'),
        ('Full-Process-Dates', 'Full Process & Dates'),
        ('Full-Process-Express-Dates', 'Full Process & Express Dates'),
    ]
    
    LOCATION_CHOICES = [
        ('Pan-India', 'Pan India'),
        ('Chennai-Only', 'Chennai Only'),
        ('Mumbai-Both-Dates', 'Mumbai-(Both Dates'),
        ('Mumbai-Delhi-Hydrabad-Chennai-Kolkata', 'Mumbai, Delhi, Hydrabad, Chennai, Kolkata'),
        ('Mumbai/Location-of-Your-Choice', 'Mumbai/Location of Your Choice'),
        ('Location-of-your-choice/Hydrabad-Chennai', 'Location of your Choice/Hydrabad or Chennai'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    visa_type = models.CharField(max_length=50, choices=VISA_CHOICES)
    service_type = models.CharField(max_length=50, choices=Service_CHOICES)
    appointment_location = models.CharField(max_length=50, choices=LOCATION_CHOICES)
    travellers = models.PositiveIntegerField(default=1)
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
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