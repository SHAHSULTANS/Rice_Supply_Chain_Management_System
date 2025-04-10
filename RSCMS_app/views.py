from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm



# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Registration Successfull")
    else:
        form = CustomUserCreationForm()
    return render(request,'auth/register.html',{'form':form})