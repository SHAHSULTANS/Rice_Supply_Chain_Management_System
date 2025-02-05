from django.contrib import admin
from django.urls import path,include
from mill import views

urlpatterns = [
    path('', views.home, name='home'),
    path('farmers/', views.farmers_list, name='farmers'),
    path('mill_manager/', views.mill_manager, name='mill_manager'),
    path('customer/', views.customer, name='customer'),
]