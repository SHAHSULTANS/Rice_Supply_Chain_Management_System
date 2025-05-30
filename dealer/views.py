from datetime import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from accounts.models import CustomUser
from dealer.forms import DealerProfileForm, PaddyStockForm
from dealer.models import DealerProfile, PaddyStock


# Create your views here.

def check_dealer(user):
    return user.is_authenticated and user.role == 'dealer'

@login_required(login_url='login')
@user_passes_test(check_dealer)
@login_required
def dealer_dashboard(request):
    dealer = get_object_or_404(DealerProfile, user=request.user)

    # Get all posts by this dealer
    posts = PaddyStock.objects.filter(dealer=dealer).order_by('-stored_since')

    # Dashboard metrics
    active_posts_count = posts.filter(is_available=True).count()
    total_quantity = posts.aggregate(total=Sum('quantity'))['total'] or 0
    avg_price = posts.aggregate(avg=Avg('price_per_mon'))['avg'] or 0

    # Count of recent orders (last 30 days)
    # recent_orders_count = Order.objects.filter(
    #     paddy__dealer=dealer,
    #     created_at__gte=timezone.now() - timezone.timedelta(days=30)
    # ).count()

    context = {
        'dealer': dealer,
        'posts': posts,
        'active_posts_count': active_posts_count,
        'total_quantity': total_quantity,
        'avg_price': round(avg_price, 2),
        'recent_orders_count': 20,
    }

    return render(request, 'dealer/dashboard.html', context)


def dealer_profile_create(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = DealerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            dealer = form.save(commit=False)
            dealer.user = user
            dealer.save()
            return redirect('login')
    else:
        form = DealerProfileForm()

    return render(request, 'dealer/dealer_profile_form.html', {'form': form})




def add_paddy_post(request):
    if request.method == 'POST':
        form = PaddyStockForm(request.POST , request.FILES)
        if form.is_valid():
            paddy_post = form.save(commit=False)
            # Get dealer profile of logged-in user
            dealer = get_object_or_404(DealerProfile, user=request.user)
            paddy_post.dealer = dealer
            paddy_post.save()
            return redirect(reverse('dealer_dashboard'))  # or your desired page
    else:
        form = PaddyStockForm()

    return render(request, 'dealer/add_paddy_post.html', {'form': form})



def see_all_paddy_posts(request):
    posts = PaddyStock.objects.filter(is_available=True).order_by('-stored_since')
    return render(request, 'dealer/paddy_posts.html', {'posts': posts})


def edit_paddy_post(request, post_id):
    post = get_object_or_404(PaddyStock, id=post_id)

    if request.method == 'POST':
        form = PaddyStockForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dealer_dashboard')
    else:
        form = PaddyStockForm(instance=post)

    return render(request, 'dealer/edit_post.html', {'form': form})




from django.contrib import messages
def delete_post(request, post_id):
    post = get_object_or_404(PaddyStock, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
    return redirect('dealer_dashboard')  



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DealerProfile
from .forms import DealerProfileEditForm

def edit_dealer_profile(request):
    dealer_profile = request.user.dealerprofile
    print(dealer_profile)
    
    
    if request.method == 'POST':
        form = DealerProfileEditForm(request.POST, instance=dealer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dealer_dashboard')
    else:
        form = DealerProfileEditForm(instance=dealer_profile)
    
    context = {
        'form': form,
        'dealer': dealer_profile
    }
    return render(request, 'dealer/edit_profile.html', context)