from django.db import models

class VisaCategory(models.Model):
    name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_price = models.DecimalField(max_digits=10, decimal_places=2)
    after_work_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_price = models.DecimalField(max_digits=10, decimal_places=2)
    after_work_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class AppointmentLocation(models.Model):
    name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    advance_price = models.DecimalField(max_digits=10, decimal_places=2)
    after_work_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name