from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def check_dealer(user):
    return user.is_authenticated and user.role == 'dealer'

@login_required(login_url='login')
@user_passes_test(check_dealer)
def dealer_dashboard(request):
    return render(request, 'RSCMS_app/dashboard.html',{'role':'dealer'})
