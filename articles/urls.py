from django.urls import path, re_path

from . import views

app_name = 'articles'
urlpatterns = [
    # Gereniar artigos
    re_path(r'^devocional/criar/?$', views.publish_articles, name='publish'),
    re_path(r'^devocional/one/(?P<article_id>\d+)/?$', views.article, name='article'),
    re_path(r'^devocional/all/?$', views.all_articles, name='all_articles'),
    re_path(r'^devocional/all/s/?$', views.search_articles, name='search_articles'),

    # Articles manager
    path('devocional/manager/', views.articles_manager, name='articles_manager'),
    path('devocional/article_verify/<int:article_id>', views.article_verify, name='article_verify'),
    path('devocional/article_unverify/<int:article_id>', views.article_unverify, name='article_unverify'),
    path('devocional/article_delete/<int:article_id>', views.article_delete, name='article_delete'),

]
