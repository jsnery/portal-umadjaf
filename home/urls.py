from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^c/editar/?$', views.carrousel_add, name='carrousel_editor'),
    re_path(r'^c/?$', views.carrousel, name='carrousel'),
    path('c/delete/<item_id>', views.carrousel_delete, name='carrousel_delete'),
]
