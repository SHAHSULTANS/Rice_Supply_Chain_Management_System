from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from .models import CustomerProfile
from .forms import CustomerProfileForm
def check_customer(user):
    return user.is_authenticated and user.role == 'customer'


@login_required(login_url='login')
@user_passes_test(check_customer)
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html',{'role':'customer'})

@login_required(login_url='login')
@user_passes_test(check_customer)
def customer_profile(request):
    customer, created =CustomerProfile.objects.get_or_create(user=request.user)
    return render(request,"customer/customer_profile.html",{'customer':customer})

@login_required(login_url='login')
@user_passes_test(check_customer)
def update_customer_profile(request):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customer_profile")
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request,"customer/update_customer_profile.html",{'form':form})
        
        
def purchase_rice(request,id):
    return HttpResponse("have to implement this part")


def explore_rice_post(request):
    return redirect("explore_all_rice_post")