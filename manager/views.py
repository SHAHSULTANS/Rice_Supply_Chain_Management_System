from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import ManagerProfile, RicePost, Purchase_paddy,PurchaseRice,PaymentForPaddy
from dealer.models import PaddyStock
from .forms import ManagerProfileForm, RicePostForm, Purchase_paddyForm, PurchaseRiceForm,PaymentForPaddyForm, PaymentForRiceForm
from decimal import Decimal
from django.db.models import Count, Sum, Avg
from customer.models import Purchase_Rice
from django.contrib import messages

import uuid
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q



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
    
    sort = request.GET.get('sort', 'recent')

    posts = PaddyStock.objects.filter(is_available=True)

    if sort == 'price_asc':
        posts = posts.order_by('price_per_mon')
    elif sort == 'price_desc':
        posts = posts.order_by('-price_per_mon')
    elif sort == 'moisture':
        posts = posts.order_by('moisture_content')
    else:  # ' By Default
        posts = posts.order_by('-stored_since')

    avg_price = posts.aggregate(avg=Avg('price_per_mon'))['avg']
    total_quantity = posts.aggregate(total=Sum('quantity'))['total'] or 0
    top_dealer = posts.values('dealer__user__username').annotate(post_count=Count('id')).order_by('-post_count').first()

    return render(request, 'dealer/paddy_posts.html', {
        'posts': posts,
        'avg_price': avg_price,
        'total_quantity': total_quantity,
        'top_dealer': top_dealer['dealer__user__username'] if top_dealer else None,
        'current_sort': sort,
    })
    # paddy_stocks = PaddyStock.objects.all().order_by('-stored_since')
    # return render(request, 'dealer/paddy_posts.html', {'posts': paddy_stocks})
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
    seling_rice = Purchase_Rice.objects.filter(rice__manager=request.user).order_by("-purchase_date")

    context = {
        "purchases_paddy": purchases_paddy,
        "purchases_rice": purchases_rice,
        "seling_rice": seling_rice,
    }

    return render(request, "manager/purchase_history.html", context)




@login_required(login_url="login")
@user_passes_test(check_manager_and_admin)
def purchase_history_seen_admin(request, id):
    manager_profile = get_object_or_404(ManagerProfile, id=id)

    purchases_paddy = Purchase_paddy.objects.filter(manager=manager_profile.user).order_by("-purchase_date")
    purchases_rice = PurchaseRice.objects.filter(manager=manager_profile.user).order_by("-purchase_date")
    seling_rice = Purchase_Rice.objects.filter(rice__manager=request.user).order_by("-purchase_date")

    context = {
        'check':1,
        "manager": manager_profile,
        "purchases_paddy": purchases_paddy,
        "purchases_rice": purchases_rice,
        "seling_rice": seling_rice,
    }

    return render(request, "manager/purchase_history.html", context)

# Mock payment Getaway for paddy
@login_required
def mock_paddy_payment(request, purchase_id):
    purchase = get_object_or_404(Purchase_paddy, pk=purchase_id, manager=request.user)

    if request.method == 'POST':
        print("post")
        form = PaymentForPaddyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount == purchase.total_price:
                # ✅ Store amount in session temporarily
                request.session['payment_amount'] = float(amount)
                return redirect('insert_phone_number', purchase_id=purchase_id)
            else:
                messages.error(request, "Amount does not match the total price.")
                return redirect('mock_paddy_payment', purchase_id=purchase_id)
    else:
        form = PaymentForPaddyForm()

    context = {
        'purchase': purchase,
        'form': form,
    }
    return render(request, 'manager/payment/mock_paddy_payment.html', context)

def insert_phone_number(request,purchase_id):
    paddy = get_object_or_404(Purchase_paddy,pk=purchase_id,manager=request.user)
    # print(paddy.manager.managerprofile.phone_number)
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        if phone_number == paddy.manager.managerprofile.phone_number:
            return redirect("send_purchases_otp",email=paddy.manager.managerprofile.user.email,purchase_id=purchase_id)
        else:
            messages.error(request,"Wrong phone number, insert the correct number")
            return redirect("insert_phone_number",purchase_id=purchase_id)
    return render(request,"manager/payment/insert_phone_number.html")


otp_storage = {}
def send_purchases_otp(request,email,purchase_id):
    otp = random.randint(100000,999999)
    otp_storage[email] = {
        'otp' : otp,
        'timestamp' : datetime.now()
    }
    subject = "Transaction OTP - RSCMS"
    message = f"Assalamu Alaikum\n\nYour OTP for transaction is: {otp}\n\nNever share your Code and PIN with anyone.\n\nRSCMS never ask for this.\n\nExpiry: within 300 seconds"
    send_mail(subject,message,settings.EMAIL_HOST_USER, [email])
    
    return redirect("insert_otp",purchase_id=purchase_id,email=email)
    
    
    
def verify_purchases_otp(request, email, purchase_id, otp):
    data = otp_storage.get(email)
    if data:
        otp_valid = data['otp'] == otp
        otp_expired = datetime.now() > data['timestamp'] + timedelta(minutes=5)

        if otp_valid and not otp_expired:
            del otp_storage[email]
            messages.success(request, "OTP verified successfully.")
            return redirect("insert_password", purchase_id=purchase_id,email=email)
        elif otp_expired:
            del otp_storage[email]
            messages.error(request, "OTP has expired. Please request a new one.")
            return redirect('insert_phone_number', purchase_id=purchase_id)
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('insert_otp', purchase_id=purchase_id, email=email)
    else:
        messages.error(request, "No OTP found for this email.")
        return redirect('insert_phone_number', purchase_id=purchase_id)


            
    # return HttpResponse("OTP")

def insert_otp(request,purchase_id,email):
    paddy = get_object_or_404(Purchase_paddy,pk=purchase_id,manager=request.user)
    if request.method == "POST":
        otp = request.POST.get("otp")
        return redirect("verify_purchases_otp",email=email,purchase_id=purchase_id,otp=otp)
    return render(request,"manager/payment/insert_otp.html",{'purchase_id':purchase_id})
    
@login_required
def insert_password(request, purchase_id, email):
    purchase = get_object_or_404(Purchase_paddy, pk=purchase_id, manager=request.user)
    paddy = purchase.paddy
    amount = request.session.get('payment_amount')  # Get from session

    if not amount:
        messages.error(request, "Payment session expired.")
        return redirect('mock_paddy_payment', purchase_id=purchase_id)

    if request.method == "POST":
        password = request.POST.get('password')
        if password == purchase.manager.managerprofile.transaction_password:
            # ✅ Now process payment
            payment = PaymentForPaddy.objects.create(
                user=request.user,
                paddy=paddy,
                amount=amount,
                transaction_id=f'MOCK-{uuid.uuid4().hex[:8]}',
                is_paid=True,
                status="Success"
            )
            purchase.payment = True
            purchase.save()

            del request.session['payment_amount']  # ✅ Clean up session
            messages.success(request, "Payment successful.")
            return redirect('mock_paddy_payment_success')
        else:
            messages.error(request, "Incorrect password.")
            return redirect("insert_password", purchase_id=purchase_id, email=email)

    return render(request, "manager/payment/insert_password.html", {
        'purchase_id': purchase_id,
        'email': email
    })


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


# Search functionality
@login_required
def search(request):
    query = request.GET.get('query')  # Matches the form field name
    rice_results = []
    paddy_results = []

    user = request.user

    if user.is_authenticated:
        if user.role in ["manager", "admin"]:
            if query:
                rice_results = RicePost.objects.filter(
                    Q(rice_name__icontains=query) |
                    Q(description__icontains=query)
                )
                paddy_results = PaddyStock.objects.filter(
                    Q(name__icontains=query)
                )

        elif user.role == "dealer":
            if query:
                paddy_results = PaddyStock.objects.filter(
                    Q(name__icontains=query)
                )

        elif user.role == "customer":
            if query:
                rice_results = RicePost.objects.filter(
                    Q(rice_name__icontains=query)
                )

    context = {
        'query': query,
        'rice_results': rice_results,
        'paddy_results': paddy_results,
    }

    return render(request, 'manager/search_results.html', context)



# Oder track for rice

@login_required
@user_passes_test(lambda u: u.role == 'manager')
def order_page(request):
    orders = Purchase_Rice.objects.filter(rice__manager=request.user).order_by("-purchase_date")
    return render(request, 'manager/order_page.html', {'orders': orders})

@login_required
# @require_POST
@user_passes_test(lambda u: u.role == 'manager')
def accept_rice_order(request, id):
    order = get_object_or_404(Purchase_Rice, id=id, rice__manager=request.user)
    if order.status == "Pending":
        order.status = "Accepted"
        order.save()
    return redirect('order_page')

@login_required
# @require_POST
@user_passes_test(lambda u: u.role == 'manager')
def update_order_status(request, id):
    order = get_object_or_404(Purchase_Rice, id=id, rice__manager=request.user)
    new_status = request.POST.get('new_status')
    if order.status == "Accepted" and new_status in ["Shipping", "Delivered"]:
        order.status = new_status
        order.save()

    if order.status == "Shipping" and new_status in [ "Delivered"]:
        order.status = new_status
        order.save()
    return redirect('order_page')



# Order and delivery track
@login_required
@user_passes_test(lambda u: u.role == 'manager')
def my_paddy_order(request):
    orders = Purchase_paddy.objects.filter(manager=request.user).order_by("-purchase_date")
    return render(request, 'manager/my_paddy_order.html', {'orders': orders})

@login_required
# @require_POST
@user_passes_test(lambda u: u.role == 'manager')
def confirm_paddy_delivery(request, id):
    order = get_object_or_404(Purchase_paddy, id=id, manager=request.user)
    if order.status == "Delivered":
        if order.payment:
            order.status = "Successful"
            order.save()
            return redirect('my_paddy_order')
        else:
            return redirect('mock_paddy_payment', id=order.id)