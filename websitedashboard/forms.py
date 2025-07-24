from django import forms
from .models import BookingDetail
from .models import Payment

class BookingDetailForm(forms.ModelForm):
    class Meta:
        model = BookingDetail
        exclude = ['user']
        fields = [
            'full_name', 'mobile_number', 'email'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control form-sec-01 fs-5 pt-2 pb-2',
                'placeholder': 'Full Name',
                'style': 'border-radius: 0 12px 12px 0; border: 1.2px solid rgba(0, 0, 0, 0.5); border-left: none !important',
                'id': 'fullName'
            }),
            
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control form-sec-01 fs-5 pt-2 pb-2',
                'placeholder': 'Mobile Number',
                'style': 'border-radius: 0 12px 12px 0; border: 1.2px solid rgba(0, 0, 0, 0.5); border-left: none !important',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-sec-01 fs-5 pt-2 pb-2',
                'placeholder': 'Email ID',
                'style': 'border-radius: 0 12px 12px 0; border: 1.2px solid rgba(0, 0, 0, 0.5); border-left: none !important',
            }),
        }

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ['user', 'booking']
        fields = ['full_name', 'email', 'payment_proof']