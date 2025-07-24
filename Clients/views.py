from django.shortcuts import render, redirect
from django.urls import reverse
from .models import BookingDetail, Payment
from .forms import BookingDetailForm, PaymentProofForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages


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
    pay_now_amount = request.GET.get('payNowAmount', 'Rs. 0')
    processing_fees = request.GET.get('ProcessingFees', 'Rs. 0')
    express_date = request.GET.get('ExpressDate', 'Rs. 0')
    pay_later_amount = request.GET.get('payLaterAmount', 'Rs. 0')
    total_amount = request.GET.get('totalAmount', 'Rs. 0')

    context = {
        'visa_type': visa_type,
        'pay_now_amount': pay_now_amount,
        'processing_fees': processing_fees,
        'express_date': express_date,
        'pay_later_amount': pay_later_amount,
        'total_amount': total_amount,
    }

    return render(request, 'clients/form.html', context)

def appointment_details(request):
    context = {
        'visa_type': request.GET.get('visa_type', ''),
        'service': request.GET.get('service', ''),
        'appointment_location': request.GET.get('location', ''),
        'travellers': request.GET.get('travelers', '1'),
        'pay_now_amount': request.GET.get('payNowAmount', 'Rs. 0'),
        'processing_fees': request.GET.get('ProcessingFees', 'Rs. 0'),
        'express_date': request.GET.get('ExpressDate', 'Rs. 0'),
        'pay_later_amount': request.GET.get('payLaterAmount', 'Rs. 0'),
        'total_amount': request.GET.get('totalAmount', 'Rs. 0'),
    }
    return render(request, 'clients/appointment_details.html', context)

def process_appointment(request):
    if request.method == 'POST':
        try:
            # Store all data in session
            request.session['booking_data'] = {
                'full_name': request.POST.get('full_name'),
                'mobile_number': request.POST.get('mobile_number'),
                'email': request.POST.get('email'),
                'visa_type': request.POST.get('visa_type'),
                'service': request.POST.get('service'),
                'appointment_location': request.POST.get('appointment_location'),
                'travellers': request.POST.get('travellers'),
                'pay_now_amount': request.POST.get('pay_now_amount'),
                'processing_fees': request.POST.get('processing_fees'),
                'express_date': request.POST.get('express_date'),
                'pay_later_amount': request.POST.get('pay_later_amount'),
                'total_amount': request.POST.get('total_amount'),
            }
            
            # Redirect to success page
            return redirect('success_page')
        except Exception as e:
            messages.error(request, f"Error processing appointment: {str(e)}")
            return redirect('appointment_details')

@login_required
def submit_payment_proof(request):
    if request.method == 'POST':
        booking_data = request.session.get('booking_data')
        if not booking_data:
            messages.error(request, "Session expired or invalid. Please start the booking process again.")
            return redirect('home')
        
        # Create BookingDetail first
        booking = BookingDetail.objects.create(
            user=request.user if request.user.is_authenticated else None,
            visa_type=booking_data.get('visa_type'),
            service_type=booking_data.get('service'),  # Make sure this matches your model field name
            appointment_location=booking_data.get('appointment_location'),
            travellers=booking_data.get('travellers', 1),
            full_name=booking_data.get('full_name'),
            mobile_number=booking_data.get('mobile_number'),
            email=booking_data.get('email'),
            # Add any other fields from booking_data that match your model
        )
        
        # Then create Payment
        payment = Payment(
            booking=booking,
            payment_proof=request.FILES.get('payment_proof'),
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            status='under_process'
        )
        payment.save()
        
        # Send email notification
        send_payment_proof_email(payment, booking)
        
        # Clear session data
        if 'booking_data' in request.session:
            del request.session['booking_data']
            
        return render(request, 'clients/payment_thankyou.html', {
            'payment': payment,
            'booking': booking
        })
    
    # If GET request, show the form with booking data
    booking_data = request.session.get('booking_data', {})
    return render(request, 'clients/success.html', {
        'full_name': booking_data.get('full_name', ''),
        'email': booking_data.get('email', ''),
        'visa_type': booking_data.get('visa_type', ''),
        'service': booking_data.get('service', ''),
        'appointment_location': booking_data.get('appointment_location', ''),
        'travellers': booking_data.get('travellers', '1'),
        'pay_now_amount': booking_data.get('pay_now_amount', 'Rs. 0'),
        'processing_fees': booking_data.get('processing_fees', 'Rs. 0'),
        'express_date': booking_data.get('express_date', 'Rs. 0'),
        'pay_later_amount': booking_data.get('pay_later_amount', 'Rs. 0'),
        'total_amount': booking_data.get('total_amount', 'Rs. 0'),
    })

def send_payment_proof_email(payment, booking):
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
        ['ankitrathod091@gmail.com','tgiusavisa@gmail.com'],
    )
    
    if payment.payment_proof:
        # Get the file content type properly
        file_content_type = None
        if hasattr(payment.payment_proof.file, 'content_type'):
            file_content_type = payment.payment_proof.file.content_type
        else:
            # Fallback to common image types if content_type isn't available
            file_name = payment.payment_proof.name.lower()
            if file_name.endswith('.png'):
                file_content_type = 'image/png'
            elif file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
                file_content_type = 'image/jpeg'
            elif file_name.endswith('.pdf'):
                file_content_type = 'application/pdf'
            else:
                file_content_type = 'application/octet-stream'
        
        # Reset file pointer to beginning after potential read operations
        payment.payment_proof.file.seek(0)
        email.attach(
            payment.payment_proof.name,
            payment.payment_proof.read(),
            file_content_type
        )
    
    email.send()


# @login_required
def success_page(request):
    if not request.user.is_authenticated:
        return redirect('account') 
    booking_data = request.session.get('booking_data', {})
    context = {
        'full_name': booking_data.get('full_name', ''),
        'email': booking_data.get('email', ''),
        'visa_type': booking_data.get('visa_type', ''),
        'service': booking_data.get('service', ''),
        'appointment_location': booking_data.get('appointment_location', ''),
        'travellers': booking_data.get('travellers', '1'),
        'pay_now_amount': booking_data.get('pay_now_amount', 'Rs. 0'),
        'processing_fees': booking_data.get('processing_fees', 'Rs. 0'),
        'express_date': booking_data.get('express_date', 'Rs. 0'),
        'pay_later_amount': booking_data.get('pay_later_amount', 'Rs. 0'),
        'total_amount': booking_data.get('total_amount', 'Rs. 0'),
    }
    return render(request, 'clients/success.html', context)

@login_required
def next_step_form(request, visa_type, full_name):
    context = {
        'visa_type': visa_type,
        'full_name': full_name.replace('-', ' ')  # Convert slug back to normal text
    }
    return render(request, 'clients/form2.html', context)