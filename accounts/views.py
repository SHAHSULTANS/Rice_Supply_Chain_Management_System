from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def profile_view(request):
    return HttpResponse("Welcome to your profile.")