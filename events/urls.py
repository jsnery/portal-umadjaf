from django.urls import path, re_path
from . import views

app_name = 'events'
urlpatterns = [

    re_path(r'^eventos/?$', views.eventos, name='eventos'),
    re_path(r'^eventos/criar/?$', views.criar_evento, name='criar_evento'),

    # Calendar manager
    path('eventos/manager/', views.eventos_manager, name='eventos_manager'),
    path('eventos/e/<int:calendar_id>', views.eventos_edit, name='eventos_edit'),
    path('eventos/d/<int:calendar_id>', views.eventos_delete, name='eventos_delete'),
]
