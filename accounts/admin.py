from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from import_export.admin import ExportMixin

from accounts.models import UserProfile

# Register your models here.
from accounts.resources import UserResource

admin.site.register(UserProfile)


class UserAdmin(ExportMixin, UserAdmin):
    resource_class = UserResource
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
