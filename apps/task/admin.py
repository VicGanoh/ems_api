from django.contrib import admin
from apps.task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "deadline",
        "status",
        "employee",
    )
