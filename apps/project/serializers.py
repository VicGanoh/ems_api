from rest_framework import serializers
from apps.employee.serializers import DepartmentSerializer, EmployeeSerializer
from apps.employee.models import Employee, Department
from apps.project.models import Project
from apps.task.models import Task

from rest_framework.exceptions import ValidationError


class ProjectSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    employees = serializers.SlugRelatedField(
        many=True, slug_field="id", queryset=Employee.objects.all()
    )

    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        employees_data = representation.get("employees", [])

        employees = []

        for employee in employees_data:
            employee_instance = Employee.objects.get(id=employee)
            employee_data = {
                "id": employee_instance.id,
                "first_name": employee_instance.user.first_name,
                "last_name": employee_instance.user.last_name,
                "email": employee_instance.user.email,
                "department": employee_instance.department.name,
            }
            employees.append(employee_data)

        representation["employees"] = employees
        return representation

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.deadline = validated_data.get("deadline", instance.deadline)
        instance.status = validated_data.get("status", instance.status)

        instance.save()
        return instance
