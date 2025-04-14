from django.urls import path
from . import views

urlpatterns = [
    path('dealer/', views.dealer_view, name='dealer'),
]