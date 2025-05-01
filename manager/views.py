from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import ManagerProfile, RicePost, Purchase_paddy,PurchaseRice,PaymentForPaddy
from dealer.models import PaddyStock
from .forms import ManagerProfileForm, RicePostForm, Purchase_paddyForm, PurchaseRiceForm,PaymentForPaddyForm, PaymentForRiceForm
from decimal import Decimal


import uuid



def check_manager(user):
    return user.is_authenticated and user.role == 'manager'
def check_manager_and_customer_and_admin(user):
    return user.is_authenticated and user.role in ['manager', 'customer','admin']
def check_manager_and_admin(user):
    return user.is_authenticated and user.role in ['manager','admin']

@login_required(login_url="login")
@user_passes_test(check_manager)
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

@login_required(login_url="login")
@user_passes_test(check_manager)
def create_rice_post(request):
    if request.method == "POST":
        form = RicePostForm(request.POST, request.FILES)
        if form.is_valid():
            rice_post = form.save(commit=False)
            rice_post.manager = request.user  # 👈 Assign the manager here
            rice_post.save()
            print("User:", request.user.username)
            print("Role:", request.user.role)
            return redirect("show_my_rice_post")
    else:
        form = RicePostForm()
    return render(request, "manager/create_rice_post.html", {'form': form})

@login_required(login_url="login")
@user_passes_test(check_manager_and_admin)
def update_rice_post(request,id):
    rice_post = get_object_or_404(RicePost,id=id)
    if request.method == "POST":
        form = RicePostForm(request.POST, request.FILES, instance=rice_post)
        if form.is_valid():
            form.save()
            return redirect("show_my_rice_post")
    else:
        form = RicePostForm(instance=rice_post)
    return render(request,"manager/update_rice_post.html",{"form":form})


@login_required(login_url="login")
@user_passes_test(check_manager_and_admin)
def delete_rice_post(request,id):
    rice_post = get_object_or_404(RicePost,id=id)
    if request.method == "POST":
        rice_post.delete()
        return redirect("show_rice_post")

@login_required(login_url="login")
@user_passes_test(check_manager_and_customer_and_admin)
def explore_all_rice_post(request):
    if request.user.role in ['admin','manager','customer']:
        rice_posts = RicePost.objects.filter( is_sold=False).order_by("-created_at")
    else:
        #TODO have to add a html file for this response
        return HttpResponse("Only admin, manager and customer can see this post")
    context = {
        "check" : 1,
        'rice_posts':rice_posts
    }
    return render(request,"manager/show_rice_post.html",context)

@login_required(login_url="login")
@user_passes_test(check_manager)
def show_my_rice_post(request):
    if request.user.role in ['manager']:
        rice_posts = RicePost.objects.filter(manager=request.user, is_sold=False).order_by("-created_at")
    else:
        #TODO have to add a html file for this response
        return HttpResponse("Only manager can see this post")
    context = {
        "check" : 2,
        'rice_posts':rice_posts
    }
    return render(request,"manager/show_rice_post.html",context)

def individual_rice_post_detail(request,id):
    rice_post = get_object_or_404(RicePost,id=id)
    return render(request,"manager/individual_rice_post_detail.html",{'post':rice_post})

@login_required(login_url="login")
@user_passes_test(check_manager_and_admin)
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


def update_manager_profile_by_admin(request,id):
    profile = get_object_or_404(ManagerProfile, pk=id)

    if request.method == "POST":
        form = ManagerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("see_all_manager")  # replace with your correct URL name
    else:
        form = ManagerProfileForm(instance=profile)

    return render(request, "manager/update_manager_profile.html", {'form': form})



@login_required(login_url="login")
@user_passes_test(check_manager)
def manager_profile(request):
    manager, created = ManagerProfile.objects.get_or_create(user=request.user)
    return render(request,"manager/manager_profile.html",{'manager':manager})



    
    
    
@login_required(login_url="login")
@user_passes_test(check_manager)
def explore_paddy_post(request):
    paddy_stocks = PaddyStock.objects.all().order_by('-stored_since')
    return render(request, 'dealer/paddy_posts.html', {'posts': paddy_stocks})
#Here update by shanto. This explore paddy_post function is used to show all paddy posts in the manager dashboard. That comes from the dealer app template.


@login_required(login_url="login")
@user_passes_test(check_manager)
def purchase_paddy(request,id):
    paddy = get_object_or_404(PaddyStock, id=id , is_available=True)
    if request.method == "POST":
        form = Purchase_paddyForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            
            if purchase.quantity_purchased > paddy.quantity:
                form.add_error('quantity_purchased', "Not enough stock available.")
                return render(request, "manager/purchase_paddy.html", {'form': form, 'paddy': paddy})
            
            purchase.manager = request.user
            purchase.paddy = paddy
            purchase.total_price = Decimal((purchase.quantity_purchased/40.0) * float(paddy.price_per_mon)) + purchase.transport_cost
            purchase.save()
            
            
            paddy.quantity=paddy.quantity -  (Decimal(purchase.quantity_purchased))
            if paddy.quantity <= 0:
                paddy.is_available = False
            paddy.save()
            return redirect("purchase_history")
    else:
        form = Purchase_paddyForm()
    return render(request, "manager/purchase_paddy.html",{'form':form , 'paddy':paddy})
    


@login_required(login_url="login")
@user_passes_test(check_manager)
def purchase_rice(request, id):
    rice = get_object_or_404(RicePost,id=id)
    if request.method == "POST":
        form = PurchaseRiceForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False) 
            
            if purchase.quantity_purchased > rice.quantity_kg:
                form.add_error('quantity_purchased', "Not enough rice available.")
                return render(request, "manager/purchase_rice.html", {'form': form, 'rice': rice})
            
            purchase.manager = request.user
            purchase.rice  = rice 
            purchase.total_price = (Decimal(purchase.quantity_purchased)*rice.price_per_kg) + purchase.delivery_cost
            purchase.save()
            rice.quantity_kg = rice.quantity_kg - purchase.quantity_purchased  
            if rice.quantity_kg <= 0:
                rice.is_sold = True  
            rice.save() 
            return redirect("purchase_history")
    else:
        form = PurchaseRiceForm() 
    return render(request, "manager/purchase_rice.html",{'form':form , 'rice':rice})


@login_required(login_url="login")
@user_passes_test(check_manager_and_admin)
def purchase_history(request):
    purchases_paddy = Purchase_paddy.objects.filter(manager=request.user).order_by("-purchase_date")
    purchases_rice = PurchaseRice.objects.filter(manager=request.user).order_by("-purchase_date")
    context = {
        "purchases_paddy" : purchases_paddy,
        "purchases_rice" : purchases_rice
    }
    
    return render(request,"manager/purchase_history.html",context)

@login_required(login_url="login")
@user_passes_test(check_manager_and_admin)
def purchase_history_seen_admin(request, id):
    manager_profile = get_object_or_404(ManagerProfile, id=id)

    purchases_paddy = Purchase_paddy.objects.filter(manager=manager_profile.user).order_by("-purchase_date")
    purchases_rice = PurchaseRice.objects.filter(manager=manager_profile.user).order_by("-purchase_date")

    context = {
        'check':1,
        "manager": manager_profile,
        "purchases_paddy": purchases_paddy,
        "purchases_rice": purchases_rice,
    }

    return render(request, "manager/purchase_history.html", context)

# Mock payment Getaway for paddy
@login_required
def mock_paddy_payment(request, purchase_id):
    purchase = get_object_or_404(Purchase_paddy, pk=purchase_id, manager=request.user)

    if request.method == 'POST':
        form = PaymentForPaddyForm(request.POST)
        paddy = purchase.paddy  # Already related through ForeignKey
        
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.paddy = paddy
            payment.transaction_id = f'MOCK-{uuid.uuid4().hex[:8]}'

            # Simulated payment logic
            if payment.amount == purchase.total_price:
                payment.is_paid = True
                payment.status = "Success"
                purchase.payment = True
                purchase.save()
                payment.save()
                return redirect('mock_paddy_payment_success')
            else:
                payment.status = "Failed"
                payment.save()
                return redirect('mock_paddy_payment_fail')
    else:
        form = PaymentForPaddyForm()

    context = {
        'purchase': purchase,
        'form': form,
    }
    return render(request, 'manager/payment/mock_paddy_payment.html', context)


@login_required
def mock_paddy_payment_success(request):
    return render(request,"manager/payment/mock_paddy_payment_success.html")
@login_required
def mock_paddy_payment_fail(request):
    return render(request,"manager/payment/mock_paddy_payment_fail.html")



# Mock payment Getaway for paddy
@login_required
def mock_rice_payment(request,rice_id):
    purchase =get_object_or_404(PurchaseRice,pk=rice_id, manager=request.user)
    if request.method == "POST":
        form = PaymentForRiceForm(request.POST)
        rice = purchase.rice
        
        if form.is_valid():
            payment= form.save(commit=False)
            payment.user = request.user
            payment.rice = rice
            payment.transaction_id = f'MOCK-{uuid.uuid4().hex[:8]}'
            if payment.amount == purchase.total_price:
                payment.is_paid = True
                payment.status = "success"
                purchase.payment = True
                payment.save()
                purchase.save()
                return redirect("mock_rice_payment_success")
            else:
                payment.status = "Failed"
                payment.save()
                return redirect("mock_rice_payment_fail")
            
        
    else:
        form = PaymentForRiceForm()
    context = {
        "form" : form,
        'purchase' : purchase
    }
    return render(request,"manager/payment/mock_rice_payment.html",context)

@login_required
def mock_rice_payment_success(request):
    return render(request,"manager/payment/mock_rice_payment_success.html")

@login_required
def mock_rice_payment_fail(request):
    return render(request,"manager/payment/mock_rice_payment_fail.html")



# @login_required
# def Mock_Payment_UI(request):
#     if request.method == 'POST':
#         amount = request.POST.get('total_amount')
#         purchase_id = request.POST.get('purchase_id')
#         purchase = get_object_or_404(Purchase_paddy, id=purchase_id)

#         return render(request, 'manager/payment/Mock_Payment_UI.html', {
#             'amount': amount,
#             'purchase': purchase,
#         })

#     return redirect('some_error_page')