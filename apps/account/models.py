from django.db import models

# Create your models here.
from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from apps.commons.models import BaseTimestamp

from apps.employee.models import Department, Employee, Salary, Address
from apps.project.models import Project
from apps.task.models import Task

import uuid


class CustomUserManager(UserManager):
    def create_user(self, email: str, password=None, **other_fields):
        if not email:
            raise ValueError("Please provide an email address")

        user = self.model(
            email=self.normalize_email(email=email),
            **other_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        user = self.create_user(email, password=password, **other_fields)

        user.is_admin = True
        user.save(using=self._db)
        return user


class Role(models.TextChoices):
    SUPER_ADMIN = "SUPER ADMIN", _("Super Admin")
    ADMIN = "ADMIN", _("Admin")
    SUPERVISOR = "SUPERVISOR", _("Supervisor")
    PAYROLL_ADMINISTRATOR = "PAYROLL ADMINISTRATOR", _("Payroll Administrator")


class CustomUser(BaseTimestamp, AbstractUser):
    id = models.UUIDField(
        _("user id"), primary_key=True, default=uuid.uuid4(), editable=False
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    other_names = models.CharField(
        _("other names"), max_length=100, blank=True, default=""
    )
    username = None
    email = models.EmailField(
        _("email address"), max_length=225, blank=False, unique=True
    )
    role = models.CharField(_("role"), max_length=21, choices=Role.choices, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        self.set_user_permissions(args, kwargs)
        super(CustomUser, self).save(*args, **kwargs)

    def set_user_permissions(self, args, kwargs):
        if self.role == Role.SUPER_ADMIN.value:
            self.is_staff = True
            self.is_superuser = True
        if self.role == Role.ADMIN.value:
            self.is_staff = True
        if self.role == Role.SUPERVISOR.value:
            self.is_staff = True
        if self.role == Role.PAYROLL_ADMINISTRATOR.value:
            self.is_staff = True
            
    
    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"
