from django.contrib import admin
from apps.project.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "deadline",
        "status",
        "department",
    )
