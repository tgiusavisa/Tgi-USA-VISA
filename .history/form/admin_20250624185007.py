from django.contrib import admin
from .models import Form, FormField, FormSubmission

class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    fields = ('label', 'field_type', 'required', 'placeholder', 'order', 
              'options', 'default_value', 'help_text', 'css_class', 'is_active')
    ordering = ('order',)

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    inlines = [FormFieldInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'is_active')
        }),
    )

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('form', 'created_at')
    list_filter = ('form', 'created_at')
    readonly_fields = ('form', 'data', 'created_at')
    search_fields = ('form__title', 'data')

    def has_add_permission(self, request):
        return False