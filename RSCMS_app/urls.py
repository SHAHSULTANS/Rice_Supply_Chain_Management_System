from django.contrib import admin
from django.urls import path, include
from RSCMS_app import views

urlpatterns = [
    path('register/',views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    
    path('dashboard/admin/',views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/manager/',views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/dealer/',views.dealer_dashboard, name='dealer_dashboard'),
    path('dashboard/customer/',views.customer_dashboard, name='customer_dashboard'),
]