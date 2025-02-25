from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "age",
        "can_data_be_shared",
        "can_be_contacted",
    )
    search_fields = ("id", "username", "email")
