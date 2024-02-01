from django.shortcuts import render
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from apps.project.serializers import ProjectSerializer
from apps.task.serializers import TaskSerializer

from apps.project.models import Project
from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.hooks import preprocess_exclude_path_format


class ListCreateProjectView(ListCreateAPIView):
    permission_classes = []
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all().order_by("name")
        project_name = self.request.query_params.get("name")
        department_name = self.request.query_params.get("department_name")

        if project_name is not None:
            queryset = queryset.filter(project_name=project_name)
        if department_name is not None:
            queryset = queryset.filter(department__name=department_name)
        return queryset

    @extend_schema(
        tags=["project"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["project"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateProjectView(RetrieveUpdateAPIView):
    permission_classes = []
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @extend_schema(
        tags=["project"],
    )
    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        tags=["project"],
    )
    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)
