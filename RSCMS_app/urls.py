from django.contrib import admin
from django.urls import path, include
from RSCMS_app import views

urlpatterns = [
    path('register/',views.register_view, name='register')
]