from django.urls import path
from apps.account import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    [
        path("auth/signup/", views.RegistrationView.as_view(), name="signup"),
        path("auth/login/", views.LoginView.as_view(), name="login"),
        path(
            "change-password/",
            views.ChangePasswordView.as_view(),
            name="change-password",
        ),
        path("users", views.ListUsersView.as_view(), name="users"),
        path("users/<uuid:pk>", views.RetrieveDestroyUserView.as_view()),
    ]
)
