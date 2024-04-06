"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.settings import base
from django.conf.urls.static import static
from apps.home import views

application_context = "api/"
version = "v1"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{application_context}{version}/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(f"{application_context}token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(f"{application_context}{version}/", include("apps.account.urls")),
    path(f"{application_context}{version}/", include("apps.employee.urls")),
    path(f"{application_context}{version}/", include("apps.project.urls")),
    path(f"{application_context}{version}/", include("apps.task.urls")),
    # API docs swagger
    path(f"{application_context}{version}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{application_context}{version}/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", views.index),
]

if base.DEBUG:
    urlpatterns += static(
        base.MEDIA_URL,
        document_root=base.MEDIA_ROOT
    )