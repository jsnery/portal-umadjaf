from django.urls import re_path, path
from . import views

app_name = 'gallery'
urlpatterns = [
    re_path(r'^gallery/?$', views.gallery, name='gallery'),
    re_path(r'^gallery/add/?$', views.add_to_gallery, name='add_to_gallery'),
    re_path(r'^gallery/manager/?$', views.gallery_marked_user_manager, name='gallery_marked_user_manager'),
    re_path(r'^gallery/search/?$', views.search_gallery, name='search_gallery'),
    path('gallery/m/<int:gallery_id>', views.mark_gallery, name='mark_gallery'),
    path('gallery/u/<int:gallery_id>', views.unmark_gallery, name='unmark_gallery'),
    path('gallery/u/<int:gallery_id>/<int:user_id>', views.check_mark_gallery, name='check_mark_gallery'),
]
