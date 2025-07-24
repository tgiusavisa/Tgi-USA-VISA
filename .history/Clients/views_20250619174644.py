from django.shortcuts import render, redirect
from .models import BookingDetail, Payment
from .forms import BookingDetailForm, PaymentProofForm
from django.contrib.auth.decorators import login_required

def appointment_form(request, visa_type):
    # Get parameters from URL
    appointment_location = request.GET.get('location', 'pan-india')
    travellers = int(request.GET.get('travelers', 1))
    
    if request.method == 'POST':
        # Store form data in session instead of saving
        form = BookingDetailForm(request.POST)
        if form.is_valid():
            request.session['booking_data'] = {
                'visa_type': visa_type,
                'appointment_location': appointment_location,
                'travellers': travellers,
                'full_name': form.cleaned_data['full_name'],
                'mobile_number': form.cleaned_data['mobile_number'],
                'email': form.cleaned_data['email']
            }
            return redirect('success_page')
    else:
        form = BookingDetailForm()
    
    context = {
        'form': form,
        'visa_type': visa_type,
        'appointment_location': appointment_location,
        'travellers': travellers,
    }
    return render(request, 'clients/form.html', context)


@login_required
def submit_payment_proof(request):
    if request.method == 'POST':
        # Get booking data from session
        booking_data = request.session.get('booking_data')
        if not booking_data:
            return redirect('home')  # Or handle missing data
        
        payment_form = PaymentProofForm(request.POST, request.FILES)
        if payment_form.is_valid():
            # Save both models
            booking = BookingDetail.objects.create(
                user=request.user if request.user.is_authenticated else None,
                **booking_data
            )
            
            payment = payment_form.save(commit=False)
            payment.booking = booking  # Link payment to booking
            payment.save()
            
            # Clear session data
            del request.session['booking_data']
            
            return render(request, 'clients/payment_thankyou.html', {
                'payment': payment
            })
    else:
        payment_form = PaymentProofForm()
    
    return render(request, 'clients/success.html', {
        'payment_form': payment_form
    })
@login_required
def success_page(request):
    return render(request, 'clients/success.html')

@login_required
def next_step_form(request, visa_type, full_name):
    context = {
        'visa_type': visa_type,
        'full_name': full_name.replace('-', ' ')  # Convert slug back to normal text
    }
    return render(request, 'clients/form2.html', context)