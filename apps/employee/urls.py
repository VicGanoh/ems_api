from django.urls import path
from apps.employee import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns(
    [
        path("addresses", views.ListCreateAddressView.as_view(), name="addresses"),
        path(
            "addresses/<uuid:pk>",
            views.RetrieveAddressView.as_view(),
            name="get_address_by_id",
        ),
        path("employees/", views.ListCreateEmployeeView.as_view(), name="employees"),
        path("employees/<uuid:pk>", views.RetrieveUpdateDeleteEmployeeView.as_view()),
        path(
            "departments/", views.ListCreateDepartmentView.as_view(), name="departments"
        ),
        path(
            "departments/<uuid:pk>", views.RetrieveUpdateDeleteDepartmentView.as_view()
        ),
        path(
            "salaries/", views.ListCreateEmployeeSalaryView.as_view(), name="salaries"
        ),
        path(
            "salaries/<uuid:pk>", views.RetrieveUpdateDeleteEmployeeSalaryView.as_view()
        ),
    ]
)
