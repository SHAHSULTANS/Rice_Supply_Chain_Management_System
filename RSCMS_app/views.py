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
            return redirect('login_view')
    else:
        form = CustomUserCreationForm()
    return render(request,'auth/register.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return HttpResponse("Login Successfully")
            # return role_based_redirect(user)
        else:
            messages.error(request,"Invalid username of password")
    else:
        form = AuthenticationForm()
    return render(request,'auth/login.html',{'form':form})

def role_based_redirect(user):
    pass