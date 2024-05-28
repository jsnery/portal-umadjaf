from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    path('users/', views.users, name='users'),
    path('delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('user_edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('users_roles/', views.users_roles, name='users_roles'),
]
