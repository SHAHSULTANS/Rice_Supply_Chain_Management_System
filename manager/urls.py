from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager_view, name='manager'),
    path('dashboard/manager/',views.manager_dashboard, name='manager_dashboard'),

]