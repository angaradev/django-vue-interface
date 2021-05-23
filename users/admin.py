from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, AutoUser, UserProfile, UserAdresses


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # list_display = ["username", "email", "is_staff"]


admin.site.register(CustomUser)
admin.site.register(AutoUser)
admin.site.register(UserProfile)
admin.site.register(UserAdresses)
