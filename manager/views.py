from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

def check_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required(login_url='login')
@user_passes_test(check_manager)
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

def create_post_rice(request):
    pass
def show_post_rice(request):
    pass

