from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)
    list_display = ("email", "username", "is_staff", "is_active", "email_verified_at", "date_joined")
    search_fields = ("email", "username")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("username", "first_name", "last_name")}),
        ("Verification", {"fields": ("email_verified_at",)}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "country_code", "updated_at")
    search_fields = ("user__email", "display_name")
