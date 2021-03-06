from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserInfo

class UserInfoInline(admin.StackedInline):
    model = UserInfo
    can_delete = False
    verbose_name_plural = 'info'

class UserAdmin(UserAdmin):
    inlines = (UserInfoInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)