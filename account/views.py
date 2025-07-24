from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from Clients.models import BookingDetail, Payment

def account(request):
    return render(request, 'account.html')

@login_required(login_url='/account/')
def dashboard(request):
    bookings = BookingDetail.objects.filter(user=request.user).order_by('-created_at').prefetch_related('payments')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'bookings': bookings,
    }
    return render(request, 'dashboard.html', context)

def logout_user(request):
    logout(request)
    return redirect('account')

def register_user(request):
    if request.method == 'POST':
        full_name = request.POST.get('full-name', '')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check for space in username
        if ' ' in username:
            return redirect(f"{reverse('account')}?status=invalid_username")

        # Split full name into first and last name
        name_parts = full_name.strip().split()
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        # Check if user exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return redirect(f"{reverse('account')}?status=exists")

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return redirect(f"{reverse('account')}?status=success")
    else:
        return redirect('account')

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        users = User.objects.filter(email=email)
        if not users.exists():
            messages.error(request, 'Invalid email or password')
            return redirect('/account/')

        user = users.first()  # Take the first matched user
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('/account/')

    return redirect('/account/')