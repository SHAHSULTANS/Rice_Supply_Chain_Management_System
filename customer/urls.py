from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/customer/',views.customer_dashboard, name='customer_dashboard'),
    path("customer_profile/",views.customer_profile,name="customer_profile"),

    path("update_customer_profile/",views.update_customer_profile,name="update_customer_profile"),
    path("update_customer_profile_by_admin/<int:id>",views.update_customer_profile_by_admin,name="update_customer_profile_by_admin"),

    path("purchase_rice_from_manager/<int:id>/",views.purchase_rice_from_manager,name="purchase_rice_from_manager"),
    path("explore_rice_post/",views.explore_rice_post,name="explore_rice_post"),
    path('rice_purchases_history/', views.rice_purchases_history, name='rice_purchases_history'),

    path("purchase_rice_from_manager/<int:id>/", views.purchase_rice_from_manager, name="purchase_rice_from_manager"),
    path("mock_customer_rice_payment/<int:purchase_id>/", views.mock_customer_rice_payment, name="mock_customer_rice_payment"),
    path("mock_customer_rice_payment_success/", views.mock_customer_rice_payment_success, name="mock_customer_rice_payment_success"),
    path("mock_customer_rice_payment_fail/", views.mock_customer_rice_payment_fail, name="mock_customer_rice_payment_fail"),


]