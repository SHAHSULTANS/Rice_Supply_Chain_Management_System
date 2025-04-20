# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = user.role
            print(role)
            
            #role for custom user models.
            if role == 'dealer':
                return redirect("dealer_profile_create", user_id=user.id)
            else:
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/auth/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return role_based_redirect(user)
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Redirect Logic
def role_based_redirect(user):
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'manager':
        return redirect('manager_dashboard')
    elif user.role == 'dealer':
        return redirect('dealer_dashboard')
    elif user.role == 'customer':
        return redirect('customer_dashboard')