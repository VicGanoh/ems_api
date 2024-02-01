from django.db import models
from apps.commons.models import BaseTimestamp, ProjectStatus
from apps.employee.models import Department, Employee

from django.utils.translation import gettext_lazy as _
import uuid


class Project(BaseTimestamp):
    id = models.UUIDField(
        _("project id"), primary_key=True, default=uuid.uuid4(), editable=False
    )
    name = models.CharField(_("project name"), max_length=100, blank=False)
    description = models.TextField(
        _("description"), max_length=225, blank=True, default=""
    )
    start_date = models.DateField(_("start date"), blank=False)
    deadline = models.DateField(_("project deadline"), blank=True)
    status = models.CharField(
        _("project status"), max_length=12, choices=ProjectStatus.choices
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="projects"
    )
    employees = models.ManyToManyField(Employee)

    class Meta:
        db_table = "projects"
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return f"Project: {self.name}, {self.status}, {self.department.name} department"
