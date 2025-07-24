from django import forms
from .models import Form, FormField

class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        form_obj = kwargs.pop('form_obj')
        super(DynamicForm, self).__init__(*args, **kwargs)
        
        for field in form_obj.fields.filter(is_active=True).order_by('order'):
            field_kwargs = {
                'required': field.required,
                'label': field.label,
                'help_text': field.help_text,
                'initial': field.default_value,
            }
            
            if field.placeholder:
                field_kwargs['widget'] = forms.TextInput(attrs={'placeholder': field.placeholder})
            
            if field.field_type == 'text':
                self.fields[field.label] = forms.CharField(**field_kwargs)
            elif field.field_type == 'number':
                self.fields[field.label] = forms.IntegerField(**field_kwargs)
            elif field.field_type == 'email':
                self.fields[field.label] = forms.EmailField(**field_kwargs)
            elif field.field_type == 'select':
                choices = [(opt, opt) for opt in field.options] if field.options else []
                self.fields[field.label] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.Select(attrs={'class': field.css_class}),
                    **field_kwargs
                )
            elif field.field_type == 'checkbox':
                self.fields[field.label] = forms.BooleanField(**field_kwargs)
            elif field.field_type == 'radio':
                choices = [(opt, opt) for opt in field.options] if field.options else []
                self.fields[field.label] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    **field_kwargs
                )
            elif field.field_type == 'textarea':
                self.fields[field.label] = forms.CharField(
                    widget=forms.Textarea,
                    **field_kwargs
                )