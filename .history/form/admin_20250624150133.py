from django.contrib import admin
from .models import Form, FormField, SelectOption, PriceItem

class SelectOptionInline(admin.TabularInline):
    model = SelectOption
    extra = 1

class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    inlines = [SelectOptionInline]

class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 1

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [FormFieldInline, PriceItemInline]
    list_display = ('name', 'title', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {'name': ('title',)}

@admin.register(FormField)
class FormFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'form', 'field_type', 'required', 'order', 'is_active', 'icon_preview')
    list_filter = ('form', 'field_type', 'is_active')
    inlines = [SelectOptionInline]

@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('label', 'form', 'value', 'is_free', 'order')
    list_filter = ('form', 'is_free')