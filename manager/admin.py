from django.contrib import admin
from .models import Congregations


# Register your models here.
class CongregationsAdmin(admin.ModelAdmin):
    ...


admin.site.register(Congregations, CongregationsAdmin)
