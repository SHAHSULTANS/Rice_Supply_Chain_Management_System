from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def check_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required(login_url='login')
@user_passes_test(check_manager)
def manager_dashboard(request):
    return render(request, 'RSCMS_app/dashboard.html', {'role': 'manager'})