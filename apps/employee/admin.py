from django.contrib import admin
from apps.employee.models import Employee, Address, Department, Salary


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "other_names",
        "last_name",
        "email",
        "phone_number",
        "age",
        "employee_status",
        "job_title",
        "hire_date",
        "user",
    )

    def first_name(self, obj):
        return obj.user.first_name

    def other_names(self, obj):
        return obj.user.other_names

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "amount",
        "employee",
        "start_date",
        "end_date",
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "city",
        "address_line1",
        "address_line2",
        "region",
        "postal_code",
    )
