from django.shortcuts import render
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from apps.task.serializers import TaskSerializer
from apps.project.serializers import ProjectSerializer
from apps.task.models import Task
from apps.project.models import Project
from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.hooks import preprocess_exclude_path_format


class ListCreateEmployeeTaskView(ListCreateAPIView):
    permission_classes = []
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @extend_schema(
        tags=["task"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["task"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateDeleteTaskView(RetrieveUpdateDestroyAPIView):
    permission_classes = []
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @extend_schema(
        tags=["task"],
    )
    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        tags=["task"],
    )
    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    @extend_schema(
        tags=["task"],
    )
    def delete(self, request, pk):
        self.destroy(request, pk)
        return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)
