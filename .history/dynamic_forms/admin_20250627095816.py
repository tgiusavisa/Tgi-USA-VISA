from django.contrib import admin
from .models import VisaCategory, ServiceType, AppointmentLocation

@admin.register(VisaCategory)
class VisaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_price', 'advance_price', 'after_work_price', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_price', 'advance_price', 'after_work_price', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)

@admin.register(AppointmentLocation)
class AppointmentLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_price', 'advance_price', 'after_work_price', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('name',)