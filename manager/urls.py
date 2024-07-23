from django.urls import path
from . import views

app_name = 'manager'
urlpatterns = [
    # Adm panel
    path('adm/', views.adm_panel, name='admin'),

    # Users manager
    path('adm/users/', views.users, name='users'),
    path('adm/delete_user/<int:user_id>', views.delete_user, name='delete_user'),
    path('adm/user_edit/<int:user_id>', views.user_edit, name='user_edit'),

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

    # Calendar manager
    path('adm/calendar/', views.calendar, name='calendar'),
    path('adm/calendar_edit/<int:calendar_id>', views.calendar_edit, name='calendar_edit'),
    path('adm/calendar_delete/<int:calendar_id>', views.calendar_delete, name='calendar_delete'),

    # Articles manager
    path('adm/articles/', views.articles, name='articles'),
    path('adm/article_verify/<int:article_id>', views.article_verify, name='article_verify'),
    path('adm/article_unverify/<int:article_id>', views.article_unverify, name='article_unverify'),
    path('adm/article_delete/<int:article_id>', views.article_delete, name='article_delete'),

]
