from django.contrib import admin
from .models import Roles, User, UserRoles, UserProfiles, IsUmadjaf


# Register your models here.
class RolesAdmin(admin.ModelAdmin):
    ...


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    ...


# Register your models here.
class UserRolesAdmin(admin.ModelAdmin):
    ...


# Register your models here.
class UserProfilesAdmin(admin.ModelAdmin):
    ...


class IsUmadjafAdmin(admin.ModelAdmin):
    ...


admin.site.register(Roles, RolesAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserRoles, UserRolesAdmin)
admin.site.register(UserProfiles, UserProfilesAdmin)
admin.site.register(IsUmadjaf, IsUmadjafAdmin)
