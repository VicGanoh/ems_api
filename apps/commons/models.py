from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class BaseTimestamp(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True


class CustomResponse:
    @staticmethod
    def success(data=None, message="", code=status.HTTP_200_OK):
        return {"status": "success", "code": code, "message": message, "data": data}

    @staticmethod
    def error(data=None, message="", code=status.HTTP_400_BAD_REQUEST):
        return {"status": "error", "code": code, "message": message, "data": data}


class ProjectStatus(models.TextChoices):
    IN_PROGRESS = "IN PROGRESS", _("In Progress")
    DONE = "DONE", _("Done")
    NOT_STARTED = "NOT STARTED", _("Not started")
    CANCELLED = "CANCELLED", _("Cancelled")


class TaskStatus(models.TextChoices):
    IN_PROGRESS = "IN PROGRESS", _("In Progress")
    DONE = "DONE", _("Done")
    NOT_STARTED = "NOT STARTED", _("Not started")
    CANCELLED = "CANCELLED", _("Cancelled")
