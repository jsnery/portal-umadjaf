from django.contrib import admin
from .models import Carrousel


class CarrouselAdmin(admin.ModelAdmin):
    ...


admin.site.register(Carrousel, CarrouselAdmin)
