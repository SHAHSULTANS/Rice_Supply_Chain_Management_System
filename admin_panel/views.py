from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AdminProfileForm
from .models import AdminProfile

# Create your views here.

def check_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required(login_url='login')
@user_passes_test(check_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html',{'role':'admin'})

def update_admin_profile(request):
    return render(request,"admin/update_admin_profile.html")

def admin_profile(request):
    admin, created = AdminProfile.objects.get_or_create(user=request.user)
    return render(request,"admin/admin_profile.html",{'admin':admin})