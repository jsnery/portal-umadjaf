from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.profile_settings, name='settings'),
    path('logout/', views.profile_logout, name='logout'),
]
