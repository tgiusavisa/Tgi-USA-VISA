from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('visa/<str:visa_type>/schedule-appointment/', views.appointment_form, name='appointment_form'),
    path('submit-payment-proof/', views.submit_payment_proof, name='submit_payment_proof'),
    path('success/', views.success_page, name='success_page'),
    path('visatype/<str:visa_type>/<str:full_name>/', views.next_step_form, name='next_step_form'),
]