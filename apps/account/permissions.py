from rest_framework import permissions
from apps.account.models import Role


class IsSuperAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_staff and request.user.is_superuser
        )


class IsSuperAdminOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_staff
            and (request.user.is_superuser or request.user.role == Role.ADMIN.value)
        )


class IsPayrollAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_staff
            and request.user.role == Role.PAYROLL_ADMINISTRATOR.value
        )
