from django.contrib import admin

from .models import Event


class CalendarAdmin(admin.ModelAdmin):
    ...


admin.site.register(Event, CalendarAdmin)
