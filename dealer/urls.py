from django.urls import path
from . import views

urlpatterns = [
    path('dealer/', views.dealer_view, name='dealer'),
    path('dashboard/dealer/',views.dealer_dashboard, name='dealer_dashboard'),

]