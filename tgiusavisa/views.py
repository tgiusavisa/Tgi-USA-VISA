from django.shortcuts import render, get_object_or_404
from websitedashboard.models import Visa, Home, Visitor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests

def home(request):
    Visitor.increment_count()
    
    visitor_count = Visitor.objects.get(pk=1).count if Visitor.objects.exists() else 0
    
    visas = Visa.objects.all()
    home = Home.objects.prefetch_related('hero_sliders','about_us', 'our_mission', 'our_goals', 'Our_vision', 'faq', 'highlights').first()
    
    return render(request, 'index.html', {'visas': visas,'home': home,'visitor_count': visitor_count})

def visitor_count(request):
    count = Visitor.objects.get(pk=1).count if Visitor.objects.exists() else 0
    return JsonResponse({'count': count})

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        
        TOGETHER_API_KEY = settings.TOGETHER_API_KEY
        API_URL = "https://api.together.xyz/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1", 
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response_data = response.json()
            
            if response.status_code == 200:
                return JsonResponse({
                    'response': response_data['choices'][0]['message']['content']
                })
            else:
                error_msg = response_data.get('error', {}).get('message', 'Unknown error')
                return JsonResponse({
                    'response': f"AI error: {error_msg}"
                }, status=response.status_code)
                
        except Exception as e:
            return JsonResponse({
                'response': "Our chatbot is currently unavailable. Please try again later."
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)