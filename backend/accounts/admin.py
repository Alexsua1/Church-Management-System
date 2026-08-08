from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Branch


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "role", "branch", "is_active")
    list_filter = ("role", "branch", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        ("Church Info", {"fields": ("role", "branch", "phone_number", "profile_photo", "dark_mode_enabled")}),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "is_headquarters")
