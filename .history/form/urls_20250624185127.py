from django.urls import path
from . import views

urlpatterns = [
    path('forms/<int:form_id>/', views.render_form, name='render_form'),
    path('api/form-fields/', views.get_form_fields, name='get_form_fields'),
]