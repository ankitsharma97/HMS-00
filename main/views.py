from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from .models import Patient, Doctor

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')

            # Check if a profile already exists for the user
            if user_type == 'patient' and not hasattr(user, 'patient'):
                Patient.objects.create(user=user, address_line1=form.cleaned_data['address_line1'], city=form.cleaned_data['city'], state=form.cleaned_data['state'], pincode=form.cleaned_data['pincode'])
            elif user_type == 'doctor' and not hasattr(user, 'doctor'):
                Doctor.objects.create(user=user, address_line1=form.cleaned_data['address_line1'], city=form.cleaned_data['city'], state=form.cleaned_data['state'], pincode=form.cleaned_data['pincode'])

            login(request, user)
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})



def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    user = request.user
    if hasattr(user, 'patient'):
        return render(request, 'patient_dashboard.html', {'user': user})
    elif hasattr(user, 'doctor'):
        return render(request, 'doctor_dashboard.html', {'user': user})
    else:
        # Handle the case where the user is not a patient or doctor
        return render(request, 'generic_dashboard.html', {'user': user})
