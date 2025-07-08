from django.shortcuts import render, get_object_or_404
from websitedashboard.models import Visa, Home, Visitor
from django.http import JsonResponse
from django.shortcuts import render
from dynamic_forms.models import FormCategory, PriceConfiguration


def home(request):
    Visitor.increment_count()
    
    visitor_count = Visitor.objects.get(pk=1).count if Visitor.objects.exists() else 0
    
    visas = Visa.objects.all()
    home = Home.objects.prefetch_related('about_us', 'our_mission', 'our_goals', 'Our_vision', 'faq', 'highlights').first()
    
    return render(request, 'index.html', {'visas': visas,'home': home,'visitor_count': visitor_count})

def visitor_count(request):
    count = Visitor.objects.get(pk=1).count if Visitor.objects.exists() else 0
    return JsonResponse({'count': count})