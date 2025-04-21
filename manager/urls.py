from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/manager/',views.manager_dashboard, name='manager_dashboard'),
    path('manager_profile/',views.manager_profile, name='manager_profile'),
    path('update_manager_profile/',views.update_manager_profile, name='update_manager_profile'),
    path('show_post_rice/',views.show_post_rice, name='show_post_rice'),
    path('create_post_rice/',views.create_post_rice, name='create_post_rice'),
    
    

]