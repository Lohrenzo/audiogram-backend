from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAccoutAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "id",
        "date_joined",
        "last_login",
        "is_artist",
        "is_admin",
    )
    search_fields = ("email", "username", "id")
    readonly_fields = ("date_joined", "last_login")
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, UserAccoutAdmin)
