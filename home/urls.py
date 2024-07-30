from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^c/add/?$', views.carrousel_add, name='carrousel_editor'),
    re_path(r'^c/?$', views.carrousel, name='carrousel'),
    re_path(r'^404/?$', views.does_not_exists, name='does_not_exists'),
    path('c/delete/<item_id>', views.carrousel_delete, name='carrousel_delete'),
]
