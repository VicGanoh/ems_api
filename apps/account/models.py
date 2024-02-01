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
        # if not first_name:
        #     raise ValueError("Please provide user first name")
        # if not last_name:
        #     raise ValueError("Please provide user last name")

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
        department_content_type = ContentType.objects.get_for_model(Department)
        employee_content_type = ContentType.objects.get_for_model(Employee)
        salary_content_type = ContentType.objects.get_for_model(Salary)
        address_content_type = ContentType.objects.get_for_model(Address)
        project_content_type = ContentType.objects.get_for_model(Project)
        task_content_type = ContentType.objects.get_for_model(Task)

        if self.role == Role.SUPER_ADMIN.value:
            self.is_staff = True
            self.is_superuser = True
            super().save(*args, **kwargs)
        if self.role == Role.ADMIN.value:
            self.is_staff = True
            super().save(*args, **kwargs)
            if department_content_type:
                department_permissions = Permission.objects.filter(
                    content_type=department_content_type
                )
                for perm in department_permissions:
                    self.user_permissions.add(perm)
            if employee_content_type:
                employee_permissions = Permission.objects.filter(
                    content_type=employee_content_type
                )
                for perm in employee_permissions:
                    self.user_permissions.add(perm)
            if salary_content_type:
                salary_permissions = Permission.objects.filter(
                    content_type=salary_content_type
                )
                for perm in salary_permissions:
                    self.user_permissions.add(perm)
            if address_content_type:
                address_permissions = Permission.objects.filter(
                    content_type=address_content_type
                )
                for perm in address_permissions:
                    self.user_permissions.add(perm)
            if project_content_type:
                project_permissions = Permission.objects.filter(
                    content_type=project_content_type
                )
                for perm in project_permissions:
                    self.user_permissions.add(perm)
            if task_content_type:
                task_permissions = Permission.objects.filter(
                    content_type=task_content_type
                )
                for perm in task_permissions:
                    self.user_permissions.add(perm)
        if self.role == Role.SUPERVISOR.value:
            self.is_staff = True
            super().save(*args, **kwargs)
            if department_content_type:
                department_permissions = Permission.objects.filter(
                    content_type=department_content_type
                )
                for perm in department_permissions:
                    if perm.codename == "view_department":
                        self.user_permissions.add(perm)
            if employee_content_type:
                employee_permissions = Permission.objects.filter(
                    content_type=employee_content_type
                )
                for perm in employee_permissions:
                    if perm.codename == "view_employee":
                        self.user_permissions.add(perm)
            if project_content_type:
                project_permissions = Permission.objects.filter(
                    content_type=project_content_type
                )
                for perm in project_permissions:
                    self.user_permissions.add(perm)
        if self.role == Role.PAYROLL_ADMINISTRATOR.value:
            self.is_staff = True
            super().save(*args, **kwargs)
            if department_content_type:
                department_permissions = Permission.objects.filter(
                    content_type=department_content_type
                )
                for perm in department_permissions:
                    if perm.codename == "view_department":
                        self.user_permissions.add(perm)
            if salary_content_type:
                salary_permissions = Permission.objects.filter(
                    content_type=salary_content_type
                )
                for perm in salary_permissions:
                    self.user_permissions.add(perm)

        super().save(*args, **kwargs)
    
    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}"
