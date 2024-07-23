from django.urls import path, re_path
from . import views

app_name = 'events'
urlpatterns = [

    re_path(r'^eventos/?$', views.eventos, name='eventos'),
    re_path(r'^eventos/criar/?$', views.criar_evento, name='criar_evento'),
]
