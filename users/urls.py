from django.urls import re_path, path
from . import views

app_name = 'users'
urlpatterns = [
    re_path(r'^login/?$', views.login_, name='login'),
    re_path(r'^register/?$', views.register, name='register'),
    re_path(r'^my/?$', views.profile, name='profile'),
    re_path(r'^in/(?P<user_id>\d+)/?$', views.other_profile, name='other_profile'),
    re_path(r'^in/notfound/?$', views.profile_does_not_exists, name='profile_does_not_exists'),
    path('settings/', views.profile_settings, name='settings'),
    path('logout/', views.profile_logout, name='logout'),
]