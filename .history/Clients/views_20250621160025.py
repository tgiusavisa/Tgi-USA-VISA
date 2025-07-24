from django.shortcuts import render, redirect
from .models import BookingDetail, Payment
from .forms import BookingDetailForm, PaymentProofForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


@login_required
def save_visa_credentials(request):
    if request.method == 'POST':
        try:
            # Get the latest booking detail for the current user
            booking = BookingDetail.objects.filter(user=request.user).latest('created_at')
            
            # Update with USA Visa credentials
            booking.usavisa_email = request.POST.get('usavisa_email')
            booking.usavisa_password = request.POST.get('usavisa_password')
            
            # Collect all security questions and answers
            security_questions = {}
            for i in range(1, 6):
                question = request.POST.get(f'question_{i}')
                answer = request.POST.get(f'answer_{i}')
                if question and answer:
                    security_questions[f'Q{i}'] = {
                        'question': question,
                        'answer': answer
                    }
            
            booking.security_questions = security_questions
            booking.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Credentials saved successfully!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


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
            
            send_payment_proof_email(payment, booking)

            del request.session['booking_data']
            return render(request, 'clients/payment_thankyou.html', {'payment': payment})
    
    payment_form = PaymentProofForm()
    return render(request, 'clients/success.html', {'payment_form': payment_form})

def send_payment_proof_email(self, payment, booking):
    subject = f'New Payment Proof Submission - {booking.full_name}'
    
    context = {
        'full_name': booking.full_name,
        'email': booking.email,
        'mobile_number': booking.mobile_number,
        'visa_type': booking.visa_type,
        'payment_proof': payment.payment_proof,
        'submission_date': payment.created_at,
    }
    
    message = render_to_string('clients/email/payment_proof_email.txt', context)
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['ankitrathod091@gmail.com'],  # Recipient email
    )
    
    # Attach the payment proof file if it exists
    if payment.payment_proof:
        email.attach(payment.payment_proof.name, payment.payment_proof.read(), payment.payment_proof.content_type)
    
    email.send()


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