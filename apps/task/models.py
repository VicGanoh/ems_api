from django.db import models
from apps.commons.models import BaseTimestamp, TaskStatus
from django.utils.translation import gettext_lazy as _
import uuid
from apps.employee.models import Employee


class Task(BaseTimestamp):
    id = models.UUIDField(
        _("task id"), primary_key=True, default=uuid.uuid4(), editable=False
    )
    name = models.CharField(_("task name"), max_length=100, blank=False)
    description = models.TextField(
        _("description"), max_length=225, blank=True, default=""
    )
    start_date = models.DateField(_("start date"), blank=False)
    deadline = models.DateField(_("task deadline"), blank=True)
    status = models.CharField(
        _("task status"), max_length=12, choices=TaskStatus.choices
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="tasks"
    )
    assigned_to = models.CharField(
        _("assigned to"), max_length=100, blank=True, default=""
    )

    class Meta:
        db_table = "tasks"
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    def save(self, *args, **kwargs):
        if self.assigned_to == "":
            self.assigned_to = self.employee.fullname
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Project: {self.employee.fullname}, {self.name}, {self.status}"
