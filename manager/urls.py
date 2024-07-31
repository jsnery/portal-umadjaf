from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [

    # Users manager
    path('adm/users/', views.users, name='users'),
    path('adm/delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('adm/user_edit/<int:user_id>', views.user_edit, name='user_edit'),
    path('adm/users/get', views.search_users, name='search_users'),

    # Roles manager
    path('adm/permissions/', views.users_roles, name='users_roles'),
    path('adm/permissions_changer/<int:user_id>', views.role_changer, name='permissions_changer'),

    # Congregation manager
    path('adm/congregations/', views.congregations, name='congregations'),
    path('adm/congregation_add/', views.congregation_add, name='congregation_add'),
    path('adm/congregation_edit/<int:congregation_id>', views.congregation_edit, name='congregation_edit'),
    path('adm/congregation_delete/<int:congregation_id>', views.congregation_delete, name='congregation_delete'),

    # Members manager
    path('adm/members/', views.members, name='members'),
    path('adm/member_positive/<int:member_id>', views.member_positive, name='member_positive'),
    path('adm/member_negative/<int:member_id>', views.member_negative, name='member_negative'),

]
