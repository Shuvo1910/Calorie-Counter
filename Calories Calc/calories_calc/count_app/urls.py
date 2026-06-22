from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('update_pwd/', views.change_password, name='change_password'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('consume_calorie/', views.consume_profile, name='consume_profile'),
    
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.update_profile, name='update_profile'),
]