from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dealer_dashboard, name='dealer_dashboard'),
    path('dealer-profile/<int:user_id>/', views.dealer_profile_create, name='dealer_profile_create'),
    path('add-post/', views.add_paddy_post, name='add_paddy_post'),
    path('marketplace/all_post', views.marketplace_paddy_posts, name='marketplace_paddy_posts'),


]