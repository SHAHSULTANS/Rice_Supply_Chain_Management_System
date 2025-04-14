from django.urls import path
from . import views

urlpatterns = [
    path('manager/', views.manager_view, name='manager'),
]