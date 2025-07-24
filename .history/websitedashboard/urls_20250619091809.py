from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views
from .views import submit_payment_proof, visa_book_page  
from .views import policy_view


urlpatterns = [
    path('about/', views.about, name='about'),
    path('visa/', views.visa, name='visa'),
    path('visa/visa-book/', visa_book_page, name='visa_book'),
    path('visa/<slug:slug>/', views.visa_detail, name='visa_detail'),
    path('book/<slug:slug>/', views.book_page, name='book_page'),
    path('submit-payment/', submit_payment_proof, name='submit_payment_proof'),
    path('policy/', policy_view, name='policy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)