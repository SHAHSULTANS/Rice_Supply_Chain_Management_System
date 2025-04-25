from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/customer/',views.customer_dashboard, name='customer_dashboard'),
    path("customer_profile/",views.customer_profile,name="customer_profile"),
    path("update_customer_profile/",views.update_customer_profile,name="update_customer_profile"),
    path("purchase_rice/<int:id>",views.purchase_rice,name="purchase_rice"),


]

