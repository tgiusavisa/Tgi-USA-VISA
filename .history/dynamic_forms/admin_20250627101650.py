# admin.py
from django.contrib import admin
from .models import FormCategory, FormField, PriceConfiguration

class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    fields = ('label', 'field_type', 'options', 'placeholder', 'required', 'order', 'is_active')

@admin.register(FormCategory)
class FormCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    inlines = [FormFieldInline]

@admin.register(PriceConfiguration)
class PriceConfigurationAdmin(admin.ModelAdmin):
    list_display = ('location', 'pay_now_price', 'pay_later_price', 'is_active')
    list_editable = ('pay_now_price', 'pay_later_price', 'is_active')