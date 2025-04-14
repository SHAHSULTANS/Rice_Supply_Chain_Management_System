from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
from django.http import HttpResponse

def admin_view(request):
    return HttpResponse("Welcome to your admin_view.")

def check_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required(login_url='login')
@user_passes_test(check_admin)
def admin_dashboard(request):
    return render(request, 'RSCMS_app/dashboard.html',{'role':'admin'})
