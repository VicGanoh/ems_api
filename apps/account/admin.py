from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from apps.account.models import CustomUser, EmailVerification
from django.utils.translation import gettext_lazy as _


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_verified",
        "role",
    )
    ordering = ("email",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_active=True)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "token",
        "used",
        "expired",
        "expires_at",
    )
    ordering = ("used", "user", "expires_at")
    list_filter = ("expired",)
