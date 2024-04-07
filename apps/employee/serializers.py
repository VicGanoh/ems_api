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
