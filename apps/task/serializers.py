from rest_framework import serializers
from apps.employee.models import Employee
from apps.task.models import Task


class TaskSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data):
        if data["assigned_to"] == "" and data["employee"] is not None:
            data["assigned_to"] = data["employee"].fullname
        return data

    def create(self, validated_data):
        task_instance = Task.objects.create(**validated_data)
        return task_instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.deadline = validated_data.get("deadline", instance.deadline)
        instance.status = validated_data.get("status", instance.status)

        instance.save()
        return instance
