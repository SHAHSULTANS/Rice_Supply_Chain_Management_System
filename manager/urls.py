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

    
    path('insert-phone-number/<int:purchase_id>/', views.insert_phone_number, name='insert_phone_number'),
    path('insert-otp/<int:purchase_id>/<str:email>/', views.insert_otp, name='insert_otp'),
    path('insert-password/<int:purchase_id>/<str:email>', views.insert_password, name='insert_password'),
    
    path("verify_purchases_otp/<str:email>/<int:purchase_id>/<int:otp>/",views.verify_purchases_otp,name="verify_purchases_otp"),
    path("send_purchases_otp/<str:email>/<int:purchase_id>/",views.send_purchases_otp,name="send_purchases_otp"),
    
    path('mock_rice_payment/<int:rice_id>/', views.mock_rice_payment, name='mock_rice_payment'),
    path('mock_rice_payment_success/', views.mock_rice_payment_success, name='mock_rice_payment_success'),
    path('mock_rice_payment_fail/', views.mock_rice_payment_fail, name='mock_rice_payment_fail'),
    
    # Search url
    path('search/',views.search, name="search"),
    
    # Rice order review page for Manager
    path('rice_orders/', views.order_page, name='order_page'),
    path('accept_rice_order/<int:id>/', views.accept_rice_order, name='accept_rice_order'),
    path('update_order_status/<int:id>/', views.update_order_status, name='update_order_status'),
    
    
    # order and delivery track
    path('my_paddy_order/', views.my_paddy_order, name='my_paddy_order'),
    path('confirm_paddy_delivery/<int:id>/', views.confirm_paddy_delivery, name='confirm_paddy_delivery'),
    
    
]