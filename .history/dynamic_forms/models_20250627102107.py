# models.py
from django.db import models

class FormCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Font Awesome icon class or image path")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Form Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class FormField(models.Model):
    FIELD_TYPES = (
        ('select', 'Dropdown Select'),
        ('text', 'Text Input'),
        ('number', 'Number Input'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Button'),
    )

    category = models.ForeignKey(FormCategory, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    options = models.TextField(blank=True, help_text="For select/radio/checkbox, separate options with new lines")
    placeholder = models.CharField(max_length=100, blank=True)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

class PriceConfiguration(models.Model):
    location = models.CharField(max_length=100, unique=True)
    pay_now_price = models.DecimalField(max_digits=10, decimal_places=2)
    pay_later_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.location} - Pay Now: {self.pay_now_price}, Pay Later: {self.pay_later_price}"