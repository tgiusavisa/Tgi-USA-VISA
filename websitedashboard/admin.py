# websitedashboard/admin.py
from django.contrib import admin
from .models import Details, AboutUs, OurMission, OurVision, OurGoals, Visa, Home, AboutUshome, OurMissionhome, OurVisionhome, OurGoalshome, faqshome, highlightshome, policy, Visitor, HeroSlider

class AboutUsInline(admin.StackedInline):
    model = AboutUs
    extra = 0

class OurMissionInline(admin.StackedInline):
    model = OurMission
    extra = 0

class OurVisionInline(admin.StackedInline):
    model = OurVision
    extra = 0

class OurGoalsInline(admin.StackedInline):
    model = OurGoals
    extra = 0

class DetailsAdmin(admin.ModelAdmin):
    inlines = [AboutUsInline, OurMissionInline, OurVisionInline, OurGoalsInline]

admin.site.register(Details, DetailsAdmin)

class VisaAdmin(admin.ModelAdmin):
    list_display = ('heading1', 'heading2', 'regular_price', 'offer_price', 'onetime_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('heading1', 'heading2', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Main Information', {
            'fields': ('heading1', 'heading2', 'description')
        }),
        ('Pricing', {
            'fields': ('regular_price', 'offer_price', 'onetime_amount')
        }),
        ('Media', {
            'fields': ('img',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css',)
        }
        js = (
            'https://cdn.tiny.cloud/1/YOUR_API_KEY/tinymce/6/tinymce.min.js',
            'js/tinymce_init.js',  # Your custom initialization file
        )

admin.site.register(Visa, VisaAdmin)

class AboutUshomeInline(admin.StackedInline):
    model = AboutUshome
    extra = 0

class OurMissionhomeInline(admin.StackedInline):
    model = OurMissionhome
    extra = 0

class OurVisionhomeInline(admin.StackedInline):
    model = OurVisionhome
    extra = 0

class OurGoalshomeInline(admin.StackedInline):
    model = OurGoalshome
    extra = 0

class faqhomeInline(admin.StackedInline):
    model = faqshome
    extra = 0

class highlightsInline(admin.StackedInline):
    model = highlightshome
    extra = 0

class HeroSliderInline(admin.StackedInline):
    model = HeroSlider
    extra = 1


class HomeAdmin(admin.ModelAdmin):
    inlines = [HeroSliderInline, AboutUshomeInline, OurMissionhomeInline, OurVisionhomeInline, OurGoalshomeInline, faqhomeInline, highlightsInline]
admin.site.register(Home, HomeAdmin)

# class BookingDetailAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'passport_id', 'mobile_number', 'email', 'date_of_birth', 'gender', 'address', 'submitted_at')
#     list_filter = ('full_name', 'passport_id', 'mobile_number', 'email', 'date_of_birth', 'gender', 'address',)
#     search_fields = ('full_name', 'passport_id', 'mobile_number', 'email', 'date_of_birth', 'gender', 'address',)
#     readonly_fields = ('full_name', 'passport_id', 'mobile_number', 'email', 'date_of_birth', 'gender', 'address',)
# admin.site.register(BookingDetail, BookingDetailAdmin)

# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'email', 'payment_status', 'submitted_at')
#     list_editable = ('payment_status',)
#     list_filter = ('payment_status',)
#     readonly_fields = ('submitted_at',)
#     search_fields = ('full_name', 'email', 'booking__passport_id')

# admin.site.register(Payment, PaymentAdmin)

class policyAdmin(admin.ModelAdmin):
    list_display = ('heading', 'description')

admin.site.register(policy, policyAdmin)

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('count',)

admin.site.register(Visitor, VisitorAdmin)