from django.urls import path
from apps.task import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    [
        path("tasks/", views.ListCreateEmployeeTaskView.as_view(), name="tasks"),
        path("tasks/<uuid:pk>", views.RetrieveUpdateDeleteTaskView.as_view()),
    ]
)
