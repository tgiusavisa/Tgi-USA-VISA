from django import forms
from .models import BookingDetail, Payment

class BookingDetailForm(forms.ModelForm):
    class Meta:
        model = BookingDetail
        fields = ['full_name', 'mobile_number', 'email', 'visa_type', 'appointment_location', 'travellers']
        widgets = {
            'visa_type': forms.HiddenInput(),
            'appointment_location': forms.HiddenInput(),
            'travellers': forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        self.visa_type = kwargs.pop('visa_type', None)
        self.appointment_location = kwargs.pop('appointment_location', None)
        self.travellers = kwargs.pop('travellers', 1)
        super().__init__(*args, **kwargs)
        
        common_attrs = {
            'class': 'form-control form-sec-01 fs-5 py-2',
            'style': 'border-radius: 0 12px 12px 0; border: 1.2px solid rgba(0, 0, 0, 0.5); border-left: none',
        }
        
        self.fields['full_name'].widget.attrs.update({
            'placeholder': 'Full Name',
            **common_attrs
        })
        self.fields['mobile_number'].widget.attrs.update({
            'placeholder': 'Mobile Number',
            **common_attrs
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email ID',
            **common_attrs
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.visa_type = self.visa_type
        instance.appointment_location = self.appointment_location
        instance.travellers = self.travellers
        if commit:
            instance.save()
        return instance
    

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_proof', 'full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
        }