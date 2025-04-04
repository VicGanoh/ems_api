from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from apps.commons.models import BaseTimestampedModel, UUIDModel


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


class CustomUser(BaseTimestampedModel, UUIDModel, AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    other_names = models.CharField(
        _("other names"), max_length=100, blank=True, default=""
    )
    username = None
    email = models.EmailField(
        _("email address"), max_length=225, blank=False, unique=True
    )
    is_verified = models.BooleanField(_("is verified"), default=False)
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


class EmailVerification(BaseTimestampedModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="email_verifications",
        verbose_name=_("user"),
    )
    token = models.CharField(
        _("verification token"),
        unique=True,
        editable=False,
        max_length=256,
        null=True,
        blank=True,
    )
    used = models.BooleanField(_("used"), default=False)
    expired = models.BooleanField(_("expired"), default=False)
    expires_at = models.DateTimeField(_("expires at"), null=True, blank=True)

    class Meta:
        db_table = "email_verifications"
        verbose_name = _("Email Verification")
        verbose_name_plural = _("Email Verifications")

    def __str__(self) -> str:
        return f"Email verification for {self.user.get_full_name}"

    def set_expiration_date(self) -> None:
        """
        Sets the expiration date for the user if it is not already set.
        The expiration date is set to 24 hours from the current time.
        """
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)

    def check_and_set_expiration(self) -> None:
        """
        Checks if the verification has expired and sets the expired status accordingly.
        """
        if self.expires_at < timezone.now():
            self.expired = True
            self.save()

    def is_expired(self) -> bool:
        """
        Checks if the verification has expired.

        Returns:
            bool: True if the verification has expired, False otherwise.
        """
        return self.expires_at < timezone.now()


class Permission(BaseTimestampedModel, UUIDModel):
    """
    Custom permission model for fine-grained access control.
    """
    name = models.CharField(_("name"), max_length=255, unique=True)
    codename = models.SlugField(_("codename"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = "permissions"
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")

    def __str__(self) -> str:
        return f"{self.name} - {self.codename}"


class Role(BaseTimestampedModel, UUIDModel):
    """
    Custom role model for fine-grained access control.
    """
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        related_name="roles",
        blank=True,
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="roles",
        verbose_name=_("created by"),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "roles"
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self) -> str:
        return self.name
