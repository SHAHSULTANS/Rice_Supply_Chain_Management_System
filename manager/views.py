from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def manager_view(request):
    return HttpResponse("Welcome to your manager_view.")