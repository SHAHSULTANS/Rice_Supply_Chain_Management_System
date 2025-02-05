from django.contrib import admin
from django.urls import path,include
from mill import views

urlpatterns = [
    path('',views.home, name="home")
]