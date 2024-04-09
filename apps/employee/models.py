from django.db import models
from apps.commons.models import BaseTimestamp

from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from datetime import datetime
import uuid
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField


class Gender(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")


class Region(models.TextChoices):
    GREATER_ACCRA = "GREATER ACCRA", _("Greater Accra")
    ASHANTI = "ASHANTI", _("Ashanti")
    EASTERN = "EASTERN", _("Eastern")
    VOLTA = "VOLTA", _("Volta")
    NORTHERN = "NORTHERN", _("Northern")
    UPPER_EAST = "UPPER EAST", _("Upper East")
    CENTRAL = "CENTRAL", _("Central")
    WESTERN = "WESTERN", _("Western")
    UPPER_WEST = "UPPER WEST", _("Upper West")
    BRONG_AHAFO = "BRONG AHAFO", _("Brong Ahafo")
    OTI_REGION = "OTI REGION", _("Oti Region")
    NORTH_EAST = "NORTH EAST", _("North East")
    WESTERN_NORTH = "WESTERN NORTH", _("Western North")
    BONO_EAST = "BONO EAST", _("Bono East")
    AHAFO = "AHAFO", _("Ahafo")
    SAVANNA = "SAVANNA", _("Savanna")


class EmployeeStatus(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    INACTIVE = "INACTIVE", _("Inactive")


class Address(BaseTimestamp):
    id = models.UUIDField(
        _("address id"), primary_key=True, default=uuid.uuid4, editable=False
    )
    address_line1 = models.CharField(_("address line 1"), max_length=100, blank=False)
    address_line2 = models.CharField(
        _("address line 2"), max_length=100, blank=True, default=""
    )
    city = models.CharField(_("city"), max_length=100, blank=False)
    region = models.CharField(
        _("region"), max_length=15, choices=Region.choices, blank=False
    )
    country = models.CharField(
        _("country"), max_length=50, choices=CountryField().choices, blank=True
    )
    postal_code = models.CharField(
        _("postal code"), max_length=50, blank=True, default=""
    )

    class Meta:
        db_table = "addresses"
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"Address: {self.city}, {self.region}"


class Department(BaseTimestamp):
    id = models.UUIDField(
        _("department id"), primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(_("department name"), max_length=225, blank=False)

    class Meta:
        db_table = "departments"
        verbose_name = _("department")
        verbose_name_plural = _("departments")

    def __str__(self):
        return f"{self.name}"


class Employee(BaseTimestamp):
    id = models.UUIDField(
        _("employee id"), primary_key=True, default=uuid.uuid4(), editable=False
    )
    user = models.OneToOneField("account.CustomUser", on_delete=models.CASCADE)
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    other_names = other_names = models.CharField(
        _("other names"), max_length=100, blank=True, default=""
    )
    date_of_birth = models.DateField(_("date of birth"), blank=False)
    gender = models.CharField(
        _("gender"), max_length=6, choices=Gender.choices, blank=False
    )
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    phone_number = PhoneNumberField(_("phone number"))
    hire_date = models.DateField(_("hire date"), blank=False)
    job_title = models.CharField(_("job title"), max_length=100, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee_status = models.CharField(
        _("employee status"), max_length=8, choices=EmployeeStatus.choices
    )

    class Meta:
        db_table = "employees"
        verbose_name = _("employee")
        verbose_name_plural = _("employees")

    @property
    def full_name(self):
        if self.user.other_names == "":
            return f"{self.user.first_name} {self.user.last_name}"
        else:
            return (
                f"{self.user.first_name} {self.user.other_names} {self.user.last_name}"
            )

    @property
    def age(self):
        employee_age = datetime.now().year - self.date_of_birth.year
        return employee_age

    def __str__(self) -> str:
        return f"{self.fullname}"


class Salary(BaseTimestamp):
    id = models.UUIDField(
        _("salary id"), primary_key=True, default=uuid.uuid4, editable=False
    )
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    amount = MoneyField(
        _("amount"), max_digits=10, decimal_places=2, default_currency="GHC"
    )
    start_date = models.DateField(_("start date"), blank=False)
    end_date = models.DateField(_("end date"), blank=False)

    class Meta:
        db_table = "salaries"
        verbose_name = _("salary")
        verbose_name_plural = _("salaries")

    def __str__(self) -> str:
        return f"{self.employee.fullname}, {self.amount}"
