from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.customer_view, name='customer'),
    path('dashboard/customer/',views.customer_dashboard, name='customer_dashboard'),

]