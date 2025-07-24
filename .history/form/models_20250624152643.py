from django.db import models
from django.utils.safestring import mark_safe

class Form(models.Model):
    name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    submit_button_text = models.CharField(max_length=50, default="Submit")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FormField(models.Model):
    FIELD_TYPES = (
        ('select', 'Dropdown Select'),
        ('text', 'Text Input'),
        ('number', 'Number Input'),
        ('email', 'Email Input'),
        ('tel', 'Phone Input'),
        ('textarea', 'Text Area'),
    )

    form = models.ForeignKey(Form, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES, default='text')
    required = models.BooleanField(default=True)
    placeholder = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    icon = models.ImageField(upload_to='form_icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

    def icon_preview(self):
        if self.icon:
            return mark_safe(f'<img src="{self.icon.url}" width="30" height="30" />')
        return "No Icon"
    icon_preview.short_description = 'Icon Preview'

class SelectOption(models.Model):
    field = models.ForeignKey(FormField, related_name='options', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.value})"

class PriceItem(models.Model):
    form = models.ForeignKey(Form, related_name='price_items', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    is_free = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label