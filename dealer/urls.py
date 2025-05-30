from django.urls import path
from . import views
from . import urls

urlpatterns = [
    path('dashboard/', views.dealer_dashboard, name='dealer_dashboard'),
    path('dealer-profile/<int:user_id>/', views.dealer_profile_create, name='dealer_profile_create'),
    path('add-post/', views.add_paddy_post, name='add_paddy_post'),
    path('marketplace/all_post', views.see_all_paddy_posts, name='marketplace_paddy_posts'),
    path('paddy/edit/<int:post_id>/', views.edit_paddy_post, name='edit_paddy_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/edit/',views.edit_dealer_profile, name='edit_dealer_profile'),
    path('orders/', views.dealer_order_list, name='dealer_order_list'),

]