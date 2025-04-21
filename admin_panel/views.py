from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def check_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required(login_url='login')
@user_passes_test(check_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html',{'role':'admin'})
