from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from apps.employee.serializers import (
    AddressSerializer,
    EmployeeSerializer,
    DepartmentSerializer,
    SalarySerializer,
)

from apps.employee.models import Address, Employee, Department, Salary
from apps.account.permissions import IsSuperAdminOrAdminUser, IsPayrollAdmin

from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.authentication import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.commons.models import CustomResponse


class ListCreateAddressView(ListCreateAPIView):
    permission_classes = [IsSuperAdminOrAdminUser]
    serializer_class = AddressSerializer

    def get_queryset(self):
        queryset = Address.objects.all()
        city = self.request.query_params.get("city")
        region = self.request.query_params.get("region")
        postal_code = self.request.query_params.get("postal_code")
        if city is not None:
            queryset = queryset.filter(city=city)
        if region is not None:
            queryset = queryset.filter(region=region)
        if postal_code is not None:
            queryset = queryset.filter(postal_code=postal_code)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    @extend_schema(
        tags=["address"],
        parameters=[
            OpenApiParameter(
                name="city",
                description="filter by city",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="region",
                description="filter by region",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="postal_code",
                description="filter by postal code",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        description="Implements an endpoint to retrieve all addresses",
        summary="Add address to  an employee",
        responses={200: AddressSerializer},
        examples=[
            OpenApiExample(
                name="Example of a successful response to retrieve all addresses",
                value=CustomResponse.success(
                    data=[
                        {
                            "id": "3f963b38-b003-45b3-8b21-7a08b55baeb1",
                            "created_at": "2023-12-14T10:30:16.224477Z",
                            "updated_at": "2023-12-22T13:22:58.885679Z",
                            "address_line1": "Tema Community 8",
                            "address_line2": "V-Road",
                            "city": "Tema",
                            "region": "GREATER ACCRA",
                            "country": "GH",
                            "postal_code": "",
                        },
                        {
                            "id": "f8e96fe2-a1cb-4e50-9f14-a664f0bcf827",
                            "created_at": "2023-12-14T11:08:35.281448Z",
                            "updated_at": "2023-12-22T13:22:45.717433Z",
                            "address_line1": "Achimota Mile 7",
                            "address_line2": "",
                            "city": "Achimota",
                            "region": "GREATER ACCRA",
                            "country": "GH",
                            "postal_code": "0233",
                        },
                        {
                            "id": "4e989be9-4f8a-4528-bb83-396d6515ef41",
                            "created_at": "2023-12-14T11:12:17.241568Z",
                            "updated_at": "2023-12-22T13:22:52.351516Z",
                            "address_line1": "Taifa Junction",
                            "address_line2": "",
                            "city": "Taifa",
                            "region": "GREATER ACCRA",
                            "country": "GH",
                            "postal_code": "0233",
                        },
                    ]
                ),
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs)
        response_data = CustomResponse.success(data=data)
        return Response(response_data)

    @extend_schema(
        tags=["address"],
        description="Implements an endpoint to create an employee",
        summary="Create an employee",
        responses={200: AddressSerializer},
        examples=[
            OpenApiExample(
                name="Example of a successful response to create an addresses",
                value=CustomResponse.success(),
                response_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response(CustomResponse.success())


class RetrieveAddressView(RetrieveAPIView):
    permission_classes = []
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    @extend_schema(
        tags=["address"],
        description="Implements an endpoint to retrieve an address from the database by specifying the address id",
        summary="Get an address",
        responses={200},
        examples=[
            OpenApiExample(
                name="Example of a successful response for retrieving an address",
                value=CustomResponse.success(),
                response_only=True,
            )
        ],
    )
    def get(self, request, pk):
        response_data = self.retrieve(request, pk)
        return Response(CustomResponse.success(data=response_data))


class ListCreateEmployeeView(ListCreateAPIView):
    permission_classes = [IsSuperAdminOrAdminUser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ["job_title", "employee_status", "gender"]
    search_fields = [
        "^first_name",
        "^last_name",
        "^email",
        "^job_title",
        "^department__name",
    ]

    def get_queryset(self):
        queryset = Employee.objects.all()
        department = self.request.query_params.get("department_name")

        if department is not None:
            queryset = queryset.filter(department__name=department)
        return queryset

    @extend_schema(
        tags=["employee"],
        description="Implements an endpoint to retrieve a list of employee from the database",
        summary="Get all employees",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["employee"],
        description="Implements an endpoint to create an employee and save it to the database",
        summary="Create employee",
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateDeleteEmployeeView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrAdminUser]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @extend_schema(
        tags=["employee"],
        description="Implements an endpoint to retrieve an employee from the database by specifying the employees id",
        summary="Get an employee",
        parameters=[
            OpenApiParameter(
                name="id",
                description="Employee id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            ),
        ],
    )
    def get(self, request, pk):
        return self.retrieve(request, pk)

    @extend_schema(
        tags=["employee"],
        description="Implements an endpoint to update an employee profile",
        summary="Update employee information",
        parameters=[
            OpenApiParameter(
                name="id",
                description="Employee id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def put(self, request, pk):
        return self.update(request, pk)

    @extend_schema(
        tags=["employee"],
        description="Implements an endpoint to delete an employee from the database",
        summary="Delete employee",
        parameters=[
            OpenApiParameter(
                name="id",
                description="Employee id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def delete(self, request, pk):
        self.destroy(request, pk)
        return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)


class ListCreateDepartmentView(ListCreateAPIView):
    permission_classes = [
        IsSuperAdminOrAdminUser,
    ]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all().order_by("name")
        department_name = self.request.query_params.get("name")

        if department_name is not None:
            queryset = queryset.filter(name=department_name)
        return queryset

    @extend_schema(
        tags=["department"],
        description="Implements an endpoint to retrieve a list of department from the database",
        summary="Get all departments",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["department"],
        description="Implements an endpoint to create a department and save it to the database",
        summary="Create department",
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateDeleteDepartmentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSuperAdminOrAdminUser]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @extend_schema(
        tags=["department"],
    )
    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        tags=["department"],
    )
    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    @extend_schema(
        tags=["department"],
    )
    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request, pk, *args, **kwargs)


class ListCreateEmployeeSalaryView(ListCreateAPIView):
    permissions_classes = [IsSuperAdminOrAdminUser | IsPayrollAdmin]
    serializer_class = SalarySerializer

    def get_queryset(self):
        queryset = Salary.objects.all().order_by("created_at")
        amount = self.request.query_params.get("amount")
        employee_department = self.request.query_params.get("employee_department")

        if amount is not None:
            queryset = queryset.filter(amount=amount)
        if employee_department is not None or amount is not None:
            queryset = queryset.filter(employee__department__name=employee_department)
        return queryset

    @extend_schema(
        tags=["salary"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["salary"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RetrieveUpdateDeleteEmployeeSalaryView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated | IsSuperAdminOrAdminUser | IsPayrollAdmin]
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer

    @extend_schema(
        tags=["salary"],
    )
    def get(self, request, pk, *args, **kwargs):
        if not IsAuthenticated():
            raise PermissionDenied("You do not have permission to perform this action.")
        return self.retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        tags=["salary"],
    )
    def put(self, request, pk):
        if not (
            IsSuperAdminOrAdminUser().has_permission(request, self)
            or IsPayrollAdmin().has_permission(request, self)
        ):
            raise PermissionDenied("You do not have permission to perform this action.")
        return self.update(request, pk)

    @extend_schema(
        tags=["salary"],
    )
    def delete(self, request, pk):
        if not (
            IsSuperAdminOrAdminUser().has_permission(request, self)
            or IsPayrollAdmin().has_permission(request, self)
        ):
            raise PermissionDenied("You do not have permission to perform this action.")
        return self.update(request, pk)
