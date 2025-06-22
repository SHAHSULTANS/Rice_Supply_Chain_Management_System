from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse
from .models import CustomerProfile, Purchase_Rice, Payment_For_Rice
from manager.models import RicePost
from .forms import PaymentForRiceForm
from decimal import Decimal
from .forms import CustomerProfileForm, PurchaseRiceForm
from django.contrib import messages


import uuid

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


def update_customer_profile_by_admin(request,id):
    customer = get_object_or_404(CustomerProfile, pk=id)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect("see_all_customers")
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request,"customer/update_customer_profile.html",{'form':form})


        
@login_required(login_url='login')
@user_passes_test(check_customer)
def purchase_rice_from_manager(request, id):
    rice = get_object_or_404(RicePost, id=id, is_sold=False)

    if request.method == "POST":
        form = PurchaseRiceForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            if purchase.quantity_purchased > rice.quantity_kg:
                form.add_error('quantity_purchased', "Not enough rice available.")
            else:
                purchase.customer = request.user
                purchase.rice = rice
                purchase.total_price = (Decimal(purchase.quantity_purchased) * rice.price_per_kg) + purchase.delivery_cost
                purchase.save()

                rice.quantity_kg -= purchase.quantity_purchased
                if rice.quantity_kg <= 0:
                    rice.is_sold = True
                rice.save()

                return redirect("mock_customer_rice_payment", purchase_id=purchase.id)
    else:
        form = PurchaseRiceForm()

    return render(request, "customer/purchase_rice.html", {'form': form, 'rice': rice})


def rice_purchases_history(request):
    purchases_rice = Purchase_Rice.objects.filter(customer=request.user).order_by("-purchase_date")
    # print(purchases_rice.payment)
    context = {
        "purchases_rice": purchases_rice
    }
    return render(request, "customer/purchase_history.html", context)

@login_required
@user_passes_test(check_customer)
def mock_customer_rice_payment(request, purchase_id):
    purchase = get_object_or_404(Purchase_Rice, pk=purchase_id, customer=request.user)

    # # Only allow payment if the order is Delivered and not already paid
    # print(purchase.payment)
    # if purchase.status != "Delivered" or  purchase.payment == True:
    #     messages.warning(request, "Payment not allowed. Order must be delivered and unpaid.")
    #     return redirect("my_order_page")

    if request.method == "POST":
        form = PaymentForRiceForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.rice = purchase.rice
            payment.transaction_id = f"CUSTMOCK-{uuid.uuid4().hex[:8]}"
            payment.amount = form.cleaned_data['amount']

            if payment.amount == purchase.total_price:
                payment.is_paid = True
                payment.status = "Success"
                purchase.payment = True
                purchase.status = "Successful"  # ✅ Update status after payment
                payment.save()
                purchase.save()
                messages.success(request, "Payment successful and order marked as received.")
                return redirect("my_order_page")
            else:
                payment.status = "Failed"
                payment.save()
                messages.error(request, "Payment failed. Amount mismatch.")
                return redirect("mock_customer_rice_payment_fail")
    else:
        form = PaymentForRiceForm(initial={'amount': purchase.total_price})

    return render(request, "customer/payment/mock_customer_rice_payment.html", {
        "form": form,
        "purchase": purchase
    })


@login_required
def mock_customer_rice_payment_success(request):
    return render(request, "customer/payment/success.html")

@login_required
def mock_customer_rice_payment_fail(request):
    return render(request, "customer/payment/fail.html")

def explore_rice_post(request):
    return redirect("explore_all_rice_post")

# Oder track
@login_required
@user_passes_test(lambda u: u.role == 'customer')
def my_order_page(request):
    orders = Purchase_Rice.objects.filter(customer=request.user).order_by("-purchase_date")
    return render(request, 'customer/my_order_page.html', {'orders': orders})

@login_required
# @require_POST
@user_passes_test(lambda u: u.role == 'customer')
def confirm_delivery(request, id):
    order = get_object_or_404(Purchase_Rice, id=id, customer=request.user)
    if order.status == "Delivered":
        if order.payment:
            order.status = "Successful"
            order.save()
            return redirect('my_order_page')
        else:
            return redirect('make_payment_for_rice', id=order.id)