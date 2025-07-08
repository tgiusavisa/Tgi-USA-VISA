from django.db import models
from django.contrib.postgres.fields import ArrayField

class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FormField(models.Model):
    FIELD_TYPES = (
        ('text', 'Text Input'),
        ('number', 'Number Input'),
        ('email', 'Email Input'),
        ('select', 'Dropdown Select'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Button'),
        ('textarea', 'Text Area'),
    )

    form = models.ForeignKey(Form, related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    placeholder = models.CharField(max_length=100, blank=True, default='', )
    order = models.PositiveIntegerField(default=0)
    options = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        null=True,
        help_text="For select/radio/checkbox fields, enter options separated by commas"
    )
    default_value = models.CharField(max_length=100, blank=True)
    help_text = models.CharField(max_length=200, blank=True)
    css_class = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label} ({self.get_field_type_display()})"

class FormSubmission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission for {self.form} at {self.created_at}"