from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from .models import ManagerProfile, RicePost
from .forms import ManagerProfileForm

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


def update_manager_profile(request):
    profile = get_object_or_404(ManagerProfile, user=request.user)

    if request.method == "POST":
        form = ManagerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("manager_profile")  # replace with your correct URL name
    else:
        form = ManagerProfileForm(instance=profile)

    return render(request, "manager/update_manager_profile.html", {'form': form})


def manager_profile(request):
    manager, created = ManagerProfile.objects.get_or_create(user=request.user)
    return render(request,"manager/manager_profile.html",{'manager':manager})
