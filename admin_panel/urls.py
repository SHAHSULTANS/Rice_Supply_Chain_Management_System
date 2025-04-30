from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/admin/',views.admin_dashboard, name='admin_dashboard'),
    path('admin_profile/',views.admin_profile, name='admin_profile'),
    path('update_admin_profile/',views.update_admin_profile, name='update_admin_profile'),

    path('forgot_password/', views.request_password_reset, name='forgot_password'),
    path('verify_otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('reset_password/<str:email>/', views.reset_password, name='reset_password'),
    
    path('change_password', views.change_password, name='change_password'),
    path('password_change_complete', views.password_change_complete, name='password_change_complete'),

]
