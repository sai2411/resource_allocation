from django.contrib import admin
from django.urls import path, include
from user import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('user.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    
]
