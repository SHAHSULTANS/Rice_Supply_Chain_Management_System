from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/manager/',views.manager_dashboard, name='manager_dashboard'),
    path('manager_profile/',views.manager_profile, name='manager_profile'),
    path('update_manager_profile/',views.update_manager_profile, name='update_manager_profile'),
    path('update_manager_profile/<int:id>/',views.update_manager_profile_by_admin, name='update_manager_profile_by_admin'),
    
    
    path('show_my_rice_post/',views.show_my_rice_post, name='show_my_rice_post'),
    path('explore_all_rice_post/',views.explore_all_rice_post, name='explore_all_rice_post'),
    path('individual_rice_post_detail/<int:id>',views.individual_rice_post_detail, name='individual_rice_post_detail'),
    
    
    path('create_rice_post/',views.create_rice_post, name='create_rice_post'),
    path('update_rice_post/<int:id>',views.update_rice_post, name='update_rice_post'),
    path('delete_rice_post/<int:id>',views.delete_rice_post, name='delete_rice_post'),
    
    path('explore_paddy_post/', views.explore_paddy_post, name='explore_paddy_post'),    
    

    path('purchase_paddy/<int:id>/', views.purchase_paddy, name='purchase_paddy'),
    path('purchase_rice/<int:id>/', views.purchase_rice, name='purchase_rice'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
    path('purchase_history_seen_admin/<int:id>', views.purchase_history_seen_admin, name='purchase_history_seen_admin'),
    
    # path('Mock_Payment_UI/', views.Mock_Payment_UI, name='Mock_Payment_UI'),
    


    path('mock_paddy_payment/<int:purchase_id>/', views.mock_paddy_payment, name='mock_paddy_payment'),    
    path('mock_paddy_payment_success/', views.mock_paddy_payment_success, name='mock_paddy_payment_success'),
    path('mock_paddy_payment_fail/', views.mock_paddy_payment_fail, name='mock_paddy_payment_fail'),

    
    path('mock_rice_payment/<int:rice_id>/', views.mock_rice_payment, name='mock_rice_payment'),
    path('mock_rice_payment_success/', views.mock_rice_payment_success, name='mock_rice_payment_success'),
    path('mock_rice_payment_fail/', views.mock_rice_payment_fail, name='mock_rice_payment_fail'),
    
    
]