from django.contrib import admin

# Register your models here.
from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from apps.account.models import CustomUser, Role
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
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
    list_display = ("id", "email", "first_name", "last_name", "is_staff", "is_verified", "role")
    ordering = ("email",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_active=True)
