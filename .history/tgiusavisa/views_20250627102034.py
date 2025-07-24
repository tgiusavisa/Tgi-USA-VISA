from django.shortcuts import render, get_object_or_404
from websitedashboard.models import Visa, Home, Visitor
from django.http import JsonResponse
from django.shortcuts import render
from dynamic_forms.models import FormCategory, PriceConfiguration

def home(request):
    Visitor.increment_count()
    visitor_count = Visitor.objects.get(pk=1).count if Visitor.objects.exists() else 0
    
    form_categories = FormCategory.objects.filter(is_active=True).prefetch_related(
        'fields').order_by('order')
    price_configurations = PriceConfiguration.objects.filter(is_active=True)
    
    context = {
        'form_categories': form_categories,
        'price_configurations': price_configurations,
        'visitor_count': visitor_count,
        # your existing context
    }
    return render(request, 'index.html', context)

def visitor_count(request):
    count = Visitor.objects.get(pk=1).count if Visitor.objects.exists() else 0
    return JsonResponse({'count': count})