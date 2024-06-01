from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    # Gereniar artigos
    path('articles/publish/', views.publish_articles, name='publish'),
    path('articles/manage/', views.manage_articles, name='manager'),
    path('articles/delete/<int:id>/', views.delete_article, name='delete'),

]
