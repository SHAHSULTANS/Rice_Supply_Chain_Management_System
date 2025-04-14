from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/dealer/',views.dealer_dashboard, name='dealer_dashboard'),

]