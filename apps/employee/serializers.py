from rest_framework import serializers
from apps.employee.models import (
    Address,
    Employee,
    Gender,
    Region,
    Department,
    Salary,
)

from django_countries.serializer_fields import CountryField
from apps.account.serializers import CustomUserSerializer
from apps.account.models import CustomUser
from djmoney.contrib.django_rest_framework import MoneyField
from django.shortcuts import get_object_or_404


class AddressSerializer(serializers.ModelSerializer):
    # TODO: employee address should be one to many
    class Meta:
        model = Address
        fields = "__all__"

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address_line1 = validated_data.get(
            "address_line1", instance.address_line1
        )
        instance.address_line2 = validated_data.get(
            "address_line2", instance.address_line2
        )
        instance.city = validated_data.get("city", instance.city)
        instance.region = validated_data.get("region", instance.region)
        instance.country = validated_data.get("country", instance.country)
        instance.postal_code = validated_data.get("postal_code", instance.postal_code)

        instance.save()
        return instance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = CustomUserSerializer()
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Employee
        fields = "__all__"

    # def create(self, validated_data):
    #     address_data = validated_data.pop("address")
    #     user_data = validated_data.pop("user")

    #     # if user_data:
    #     #     user_instance = get_object_or_404(CustomUser, id=user_data.id)
    #     #     validated_data["user"] = user_instance

    #     # if user_data is not None:
    #     #     validated_data["first_name"] = user_instance.first_name
    #     #     validated_data["last_name"] = user_instance.last_name
    #     #     validated_data["email"] = user_instance.email

    #     address_instance = Address.objects.create(**address_data)
    #     user_instance = CustomUser.objects.create_user(**user_data)
    #     employee_instance = Employee.objects.create(
    #         user=user_instance, address=address_instance, **validated_data
    #     )

    #     return employee_instance

    # def update(self, instance, validated_data):
    #     address_data = validated_data.pop("address")

    #     instance.address.address_line1 = address_data.get(
    #         "address_line1", instance.address.address_line1
    #     )
    #     instance.address.address_line2 = address_data.get(
    #         "address_line2", instance.address.address_line2
    #     )
    #     instance.address.city = address_data.get("city", instance.address.city)
    #     instance.address.region = address_data.get("region", instance.address.region)
    #     instance.address.postal_code = address_data.get(
    #         "postal_code", instance.address.postal_code
    #     )

    #     instance.phone_number = validated_data.get(
    #         "phone_number", instance.phone_number
    #     )
    #     instance.job_title = validated_data.get("job_title", instance.job_title)

    #     instance.save()
    #     return instance


class SalarySerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    amount = MoneyField(max_digits=10, decimal_places=2)

    class Meta:
        model = Salary
        fields = "__all__"

    # def update(self, instance, validated_data):
    #     instance.amount = validated_data.get("amount", instance.amount)
    #     instance.start_date = validated_data.get("start_date", instance.start_date)
    #     instance.end_date = validated_data.get("end_date", instance.end_date)

    #     instance.save()
    #     return instance
