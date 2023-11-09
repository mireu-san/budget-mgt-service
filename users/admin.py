from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "email",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )

    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_admin",
    )
    list_display_links = (
        "id",
        "username",
        "email",
    )

    readonly_fields = (
        "last_login",
        "date_joined",
    )
