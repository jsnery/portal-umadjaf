from django.contrib import admin
from .models import Gallery, GalleryMarked, GalleryMarkedUser


# Register your models here.
class GalleryAdmin(admin.ModelAdmin):
    ...


class GalleryMarkedAdmin(admin.ModelAdmin):
    ...


class GalleryMarkedUserAdmin(admin.ModelAdmin):
    ...


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryMarked, GalleryMarkedAdmin)
admin.site.register(GalleryMarkedUser, GalleryMarkedUserAdmin)
