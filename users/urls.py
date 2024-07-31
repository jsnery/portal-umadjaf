from django.urls import re_path, path
from . import views

app_name = 'users'
urlpatterns = [
    # Login, register and profile
    re_path(r'^login/?$', views.login_, name='login'),
    re_path(r'^register/?$', views.register, name='register'),
    re_path(r'^my/?$', views.profile, name='profile'),
    re_path(
        r'^in/(?P<other_user_id>\d+)/?$',
        views.other_profile,
        name='other_profile'
        ),
    path('w/<other_user_id>/', views.redirect_whatsapp, name='redirect_whatsapp'),
    re_path(
        r'^in/notfound/?$',
        views.profile_does_not_exists,
        name='profile_does_not_exists'
        ),

    # Profile settings and logout
    path('settings/', views.profile_settings, name='settings'),
    path('logout/', views.profile_logout, name='logout'),
]
