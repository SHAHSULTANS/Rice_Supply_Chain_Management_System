from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/manager/',views.manager_dashboard, name='manager_dashboard'),
    path('manager_profile/',views.manager_profile, name='manager_profile'),
    path('update_manager_profile/',views.update_manager_profile, name='update_manager_profile'),
    
    
    path('show_my_rice_post/',views.show_my_rice_post, name='show_my_rice_post'),
    path('explore_all_rice_post/',views.explore_all_rice_post, name='explore_all_rice_post'),
    path('individual_rice_post_detail/<int:id>',views.individual_rice_post_detail, name='individual_rice_post_detail'),
    path('create_rice_post/',views.create_rice_post, name='create_rice_post'),
    path('update_rice_post/<int:id>',views.update_rice_post, name='update_rice_post'),
    path('delete_rice_post/<int:id>',views.delete_rice_post, name='delete_rice_post'),
    
path('explore_paddy_post/', views.explore_paddy_post, name='explore_paddy_post'),    
    

    path('purchase_paddy/<int:id>/', views.purchase_paddy, name='purchase_paddy'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('make_payment/<int:id>/', views.make_payment, name='make_payment'),
    
    
]