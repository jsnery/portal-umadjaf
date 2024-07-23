from django.urls import path, re_path

from . import views

app_name = 'articles'
urlpatterns = [
    # Gereniar artigos
    re_path(r'^devocional/criar/?$', views.publish_articles, name='publish'),
    re_path(r'^devocional/one/(?P<article_id>\d+)/?$', views.article, name='article'),
    re_path(r'^devocional/all/?$', views.all_articles, name='all_articles'),
    re_path(r'^devocional/all/s/?$', views.search_articles, name='search_articles'),

]
