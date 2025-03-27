from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import status
import uuid
from django_countries.fields import CountryField


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


class UUIDModel(models.Model):
    id = models.UUIDField(_("ID"), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseTimestampedModel(models.Model):
    created_at = models.DateTimeField(
        _("created at"), auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class BaseAddress(BaseTimestampedModel, UUIDModel):
    address_line1 = models.CharField(
        _("address line 1"), max_length=100, blank=True, default=""
    )
    address_line2 = models.CharField(
        _("address line 2"), max_length=100, blank=True, default=""
    )
    city = models.CharField(_("city"), max_length=100, blank=True, default="")
    region = models.CharField(_("region"), max_length=15, blank=True)
    country = models.CharField(
        _("country"),
        max_length=50,
        choices=CountryField().choices,
        blank=True,
        default="",
    )
    postal_code = models.CharField(
        _("postal code"), max_length=50, blank=True, default=""
    )

    class Meta:
        abstract = True
        ordering = ("pk",)
        verbose_name = _("Address")
        verbose_name_plural = _("Address")
