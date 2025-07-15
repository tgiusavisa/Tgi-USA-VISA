from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Form, FormSubmission
from .forms import DynamicForm

def render_form(request, form_id):
    form_obj = get_object_or_404(Form, pk=form_id, is_active=True)
    
    if request.method == 'POST':
        dynamic_form = DynamicForm(request.POST, form_obj=form_obj)
        if dynamic_form.is_valid():
            # Save the form submission
            FormSubmission.objects.create(
                form=form_obj,
                data=dynamic_form.cleaned_data
            )
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': dynamic_form.errors})
    else:
        dynamic_form = DynamicForm(form_obj=form_obj)
    
    return render(request, 'form/dynamic_form.html', {
        'form_obj': form_obj,
        'dynamic_form': dynamic_form
    })

def get_form_fields(request):
    form_id = request.GET.get('form_id')
    form_obj = get_object_or_404(Form, pk=form_id, is_active=True)
    
    fields_data = []
    for field in form_obj.fields.filter(is_active=True).order_by('order'):
        field_data = {
            'label': field.label,
            'type': field.field_type,
            'required': field.required,
            'placeholder': field.placeholder,
            'options': field.options if field.options else [],
            'default_value': field.default_value,
            'help_text': field.help_text,
            'css_class': field.css_class,
        }
        fields_data.append(field_data)
    
    return JsonResponse({'fields': fields_data})