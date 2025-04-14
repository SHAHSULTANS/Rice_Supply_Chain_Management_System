from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def manager_view(request):
    return HttpResponse("Welcome to your manager_view.")

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def check_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required(login_url='login')
@user_passes_test(check_manager)
def manager_dashboard(request):
    return render(request, 'RSCMS_app/dashboard.html', {'role': 'manager'})