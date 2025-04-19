from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse

from accounts.models import CustomUser
from dealer.forms import DealerProfileForm, PaddyStockForm
from dealer.models import DealerProfile, PaddyStock


# Create your views here.

def check_dealer(user):
    return user.is_authenticated and user.role == 'dealer'

@login_required(login_url='login')
@user_passes_test(check_dealer)
def dealer_dashboard(request):
    dealer = get_object_or_404(DealerProfile, user=request.user)
    
    posts = PaddyStock.objects.filter(dealer=dealer).order_by('-stored_since')
    return render(request, 'dealer/dashboard.html', {'dealer': dealer, 'posts': posts})


def dealer_profile_create(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = DealerProfileForm(request.POST)
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
        form = PaddyStockForm(request.POST)
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



def marketplace_paddy_posts(request):
    posts = PaddyStock.objects.filter(is_available=True).order_by('-stored_since')
    return render(request, 'dealer/paddy_posts.html', {'posts': posts})