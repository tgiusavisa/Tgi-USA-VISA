from django.shortcuts import get_object_or_404, render, redirect
from websitedashboard.models import Details, Visa, policy
from django.contrib.auth.decorators import login_required
# from .forms import BookingDetailForm, PaymentProofForm
# from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def about(request):
    details = Details.objects.prefetch_related('about_us', 'our_mission', 'our_goals', 'Our_vision').first()
    return render(request, 'about/about.html', {'details': details})

def visa(request):   
    visas = Visa.objects.all() 
    return render(request, 'visa/visa.html', {'visas': visas})

def visa_detail(request, slug):
    visa = get_object_or_404(Visa, slug=slug)
    return render(request, 'visa/visa_detail.html', {'visa': visa})

def visa_book_page(request):
    visas = Visa.objects.all()
    return render(request, 'book/1page.html', {'visas': visas})

# @login_required(login_url='/accounts/login/')
# def book_page(request, slug):
#     visa = get_object_or_404(Visa, slug=slug)
#     if request.method == 'POST':
#         form = BookingDetailForm(request.POST, request.FILES)
#         if form.is_valid():
#             request.session['booking_data'] = {
#                 'full_name': form.cleaned_data['full_name'],
#                 'mobile_number': form.cleaned_data['mobile_number'],
#                 'email': form.cleaned_data['email'],
#             }
#             return render(request, 'clients/success.html', {'visa': visa})
#     else:
#         form = BookingDetailForm()
#     return render(request, 'book/1page.html', {'form': form, 'visa': visa})

# def submit_payment_proof(request):
#     if request.method == 'POST':
#         booking_data = request.session.get('booking_data')
#         if not booking_data:
#             logger.warning("No booking data found in session")
#             return redirect('book_page', slug=request.session.get('visa_slug'))

#         booking_form = BookingDetailForm(booking_data, request.FILES)
#         if booking_form.is_valid():
#             try:
#                 booking = booking_form.save()
#                 logger.info(f"Booking saved for {booking.full_name}")
#             except Exception as e:
#                 logger.error(f"Error saving booking: {str(e)}")
#                 return redirect('book_page', slug=request.session.get('visa_slug'))

#             payment_form = PaymentProofForm(request.POST, request.FILES)
#             if payment_form.is_valid():
#                 payment = payment_form.save(commit=False)
#                 payment.booking = booking
#                 payment.save()
                
#                 if 'booking_data' in request.session:
#                     del request.session['booking_data']

#                 try:
#                     send_customer_email(booking, payment)
#                     send_admin_email(booking, payment)
#                 except Exception as e:
#                     logger.error(f"Email processing failed: {str(e)}")

#                 return render(request, 'book/payment_success.html')

#     return redirect('success_page')

# def send_customer_email(booking, payment):
#     try:
#         subject = "Payment Proof Received - TGI USA Visa Helpline"
#         context = {'booking': booking, 'payment': payment}
#         html_message = render_to_string('emails/payment_received_customer.html', context)
#         plain_message = strip_tags(html_message)
        
#         send_mail(
#             subject,
#             plain_message,
#             settings.DEFAULT_FROM_EMAIL,
#             [booking.email],
#             html_message=html_message,
#             fail_silently=False
#         )
#         return True
#     except Exception as e:
#         logger.error(f"Customer email failed: {str(e)}")
#         return False

# def send_admin_email(booking, payment):
#     try:
#         if not hasattr(settings, 'ADMIN_EMAIL'):
#             raise ValueError("ADMIN_EMAIL not configured in settings")
            
#         admin_email = settings.ADMIN_EMAIL
#         subject = f"New Payment Proof: {booking.full_name}"
#         context = {'booking': booking, 'payment': payment}
#         html_message = render_to_string('emails/payment_received_admin.html', context)
#         plain_message = strip_tags(html_message)
        
#         send_mail(
#             subject,
#             plain_message,
#             settings.DEFAULT_FROM_EMAIL,
#             [admin_email],
#             html_message=html_message,
#             fail_silently=False
#         )
#         return True
#     except Exception as e:
#         logger.error(f"Admin email failed: {str(e)}")
#         return False

def policy_view(request):
    policies = policy.objects.all()
    return render(request, 'policy.html', {'policies': policies})