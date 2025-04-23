from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/admin/',views.admin_dashboard, name='admin_dashboard'),
    path('admin_profile/',views.admin_profile, name='admin_profile'),
    path('update_admin_profile/',views.update_admin_profile, name='update_admin_profile'),

]