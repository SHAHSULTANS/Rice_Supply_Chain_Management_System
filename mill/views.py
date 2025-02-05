from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request, 'mill/home.html')
def farmers_list(request):
    return render(request, 'mill/farmer.html')
def mill_manager(request):
    return render(request, 'mill/mill_manager.html')
def customer(request):
    return render(request, 'mill/customer.html')