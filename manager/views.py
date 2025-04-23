from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import ManagerProfile, RicePost
from .forms import ManagerProfileForm, RicePostForm

def check_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required(login_url='login')
@user_passes_test(check_manager)
def manager_dashboard(request):
    return render(request, 'manager/dashboard.html')

@login_required(login_url='login')
def create_rice_post(request):
    if request.method == "POST":
        form = RicePostForm(request.POST, request.FILES)
        if form.is_valid():
            rice_post = form.save(commit=False)
            rice_post.manager = request.user  # 👈 Assign the manager here
            rice_post.save()
            print("User:", request.user.username)
            print("Role:", request.user.role)
            return redirect("show_rice_post")
    else:
        form = RicePostForm()
    return render(request, "manager/create_rice_post.html", {'form': form})

@login_required(login_url='login')
def update_rice_post(request,id):
    rice_post = get_object_or_404(RicePost,id=id)
    if request.method == "POST":
        form = RicePostForm(request.POST, request.FILES, instance=rice_post)
        if form.is_valid():
            form.save()
            return redirect("show_rice_post")
    else:
        form = RicePostForm(instance=rice_post)
    return render(request,"manager/update_rice_post.html",{"form":form})

@login_required(login_url='login')
def show_rice_post(request):
    if request.user.role in ['admin','manager']:
        rice_posts = RicePost.objects.filter( is_sold=False).order_by("-created_at")
    else:
        #TODO have to add a html file for this response
        return HttpResponse("Only admin and manager can see this post")
    return render(request,"manager/show_rice_post.html",{'rice_posts':rice_posts})


@login_required(login_url='login')
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


@login_required(login_url='login')
def manager_profile(request):
    manager, created = ManagerProfile.objects.get_or_create(user=request.user)
    return render(request,"manager/manager_profile.html",{'manager':manager})


@login_required(login_url='login')
def explore_paddy_post(request):
    return redirect("marketplace_paddy_posts")



