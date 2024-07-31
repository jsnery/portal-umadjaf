from django.urls import re_path, path
from . import views

app_name = 'gallery'
urlpatterns = [
    # Gallery
    re_path(
        r'^gallery/?$',
        views.gallery,
        name='gallery'
    ),
    # Gallery Add
    re_path(
        r'^gallery/add/?$',
        views.add_to_gallery,
        name='add_to_gallery'
    ),
    # Gallery Search
    re_path(
        r'^gallery/search/?$',
        views.search_gallery,
        name='search_gallery'
    ),
    # Gallery Manager
    re_path(
        r'^gallery/manager/?$',
        views.gallery_manager,
        name='gallery_manager'
    ),
    # Gallery Delete
    path(
        'gallery/manager/d/<int:photo_id>',
        views.gallery_photo_delete,
        name='gallery_photo_delete'
    ),


    # Gallery Marked User Manager
    re_path(
        r'^gallery/m/manager/?$',
        views.gallery_marked_user_manager,
        name='gallery_marked_user_manager'
    ),
    # Gallery Mark
    path(
        'gallery/m/<int:gallery_id>',
        views.mark_gallery,
        name='mark_gallery'
    ),
    # Gallery Unmark
    path(
        'gallery/u/<int:gallery_id>',
        views.unmark_gallery,
        name='unmark_gallery'
    ),
    # Gallery Marked
    path(
        'gallery/u/<int:gallery_id>/<int:user_id>',
        views.check_mark_gallery,
        name='check_mark_gallery'
    ),
]
