from django.urls import path
from apps.project import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    [
        path("projects/", views.ListCreateProjectView.as_view(), name="projects"),
        path("projects/<uuid:pk>", views.RetrieveUpdateProjectView.as_view()),
    ]
)
