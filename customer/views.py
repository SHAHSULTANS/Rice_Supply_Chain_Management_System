from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def check_customer(user):
    return user.is_authenticated and user.role == 'customer'


@login_required(login_url='login')
@user_passes_test(check_customer)
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html',{'role':'customer'})
