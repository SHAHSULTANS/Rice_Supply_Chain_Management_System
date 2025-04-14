from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/customer/',views.customer_dashboard, name='customer_dashboard'),

]