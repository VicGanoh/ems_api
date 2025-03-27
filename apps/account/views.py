from django.shortcuts import redirect
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView
from apps.account.serializers import (
    CustomUserSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)
from apps.account.models import CustomUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.account import permissions
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.commons.models import CustomResponse
from rest_framework.exceptions import NotFound
from django.conf import settings
import google_auth_oauthlib.flow
import jwt

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class RegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @extend_schema(
        tags=["auth"],
        description="Implements an endpoint to create a new user",
        summary="Create a user",
        request=CustomUserSerializer,
        responses={200: CustomUserSerializer},
        examples=[
            OpenApiExample(
                name="Example of creating a user successfully response",
                value=CustomResponse.success(message="User created successfully"),
                request_only=False,
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        response_data = CustomResponse.success(
            data=None, message="User created successfully"
        )
        return Response(response_data)


class LoginView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    @extend_schema(
        tags=["auth"],
        description="Implements an endpoint to login a user",
        summary="Login",
        responses={200: LoginSerializer},
        examples=[
            OpenApiExample(
                name="Example of a successful login response",
                description="After a successful login, the response returns an access token for authenticating the client application to access specific resources on the resource owner's behalf",
                value=CustomResponse.success(
                    data={"access": "string"},
                ),
                response_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            response_data = CustomResponse.error(
                message="Invalid credentials", code=status.HTTP_401_UNAUTHORIZED
            )
            return Response(response_data)

        refresh = RefreshToken.for_user(user)
        refresh["role"] = CustomUserSerializer(user).data.get("role")
        response_data = CustomResponse.success(
            data={"refresh": f"{refresh}", "access": f"{refresh.access_token}"},
        )

        return Response(response_data)


class OAuth2LoginInView(ListAPIView):
    permission_classes = [AllowAny]

    @extend_schema(
        tags=["auth"],
        description="Implements an endpoint for third party authentication (OAuth 2.0)",
        summary="google login authorization",
    )
    def get(self, request, *args, **kwargs):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "./authentication/client_secret.json",
            scopes=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE,
        )

        flow.redirect_uri = settings.REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", state=settings.STATE
        )

        return redirect(authorization_url)


class OAuth2Callback(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    @extend_schema(
        tags=["auth"],
    )
    def get(self, request):
        auth_code = request.GET.get("code")
        if not auth_code:
            return Response(
                CustomResponse.error(message="Authorisation code is missing.")
            )

        state = request.GET.get("state")
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            "./authentication/client_secret.json",
            scopes=settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE,
            state=state,
        )

        flow.redirect_uri = settings.REDIRECT_URI

        authorisation_response = request.build_absolute_uri()

        flow.fetch_token(code=auth_code, authorisation_response=authorisation_response)
        credentials = flow.credentials
        request.session["credentials"] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
        }

        decoded_token = jwt.decode(
            jwt=credentials.id_token, options={"verify_signature": False}
        )
        user_email = decoded_token.get("email")
        first_name = decoded_token.get("given_name")
        last_name = decoded_token.get("family_name")

        user, created = CustomUser.objects.get_or_create(
            first_name=first_name, last_name=last_name, email=user_email
        )

        if created:
            print("================================================================")
            print("User created successfully")

        serializer = CustomUserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        print("================================================================")
        print("Access token: ", access_token)
        return redirect("tasks")


class ChangePasswordView(CreateAPIView):
    permission_classes = []
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        tags=["auth"],
        description="Implements an endpoint to change the password of a user",
        summary="Change the password of a user",
        responses={200: ChangePasswordSerializer},
        examples=[
            OpenApiExample(
                name="Example of a successful password update response",
                value=CustomResponse.success(message="Password changed successfully"),
                response_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            confirm_new_password = serializer.validated_data["confirm_new_password"]

            if not request.user.check_password(old_password):
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=CustomResponse.error(message="Old password is incorrect"),
                )

            if new_password != confirm_new_password:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=CustomResponse.error(
                        message="New password and confirm password do not match"
                    ),
                )

            request.user.set_password(new_password)
            request.user.save()
            response_data = CustomResponse.success(
                message="Password changed successfully"
            )

            return Response(response_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsersView(ListAPIView):
    permission_classes = [permissions.IsSuperAdminOrAdminUser | IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        email = self.request.query_params.get("email")

        if first_name is not None:
            queryset = queryset.filter(first_name=first_name)
        if last_name is not None:
            queryset = queryset.filter(last_name=last_name)
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    @extend_schema(
        tags=["user"],
        parameters=[
            OpenApiParameter(
                name="first_name",
                description="Filter by first name",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="last_name",
                description="Filter by last name",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="email",
                description="Filter by email",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        description="Implements an endpoint for retrieve all users",
        summary="Get all users",
        responses={200: CustomUserSerializer},
        examples=[
            OpenApiExample(
                name="Example of a successful response after retrieving all users",
                value=CustomResponse.success(
                    data=[
                        {
                            "id": "0b0fd774-44fd-43ec-b9cf-51f055c97f00",
                            "first_name": "Kofi",
                            "last_name": "Ganoh",
                            "email": "kof@mail.com",
                            "role": "ADMIN",
                            "created_at": "2023-12-14T10:20:36.780216Z",
                            "updated_at": "2023-12-14T10:20:36.782908Z",
                        },
                        {
                            "id": "c8e339a3-19ee-467a-9d7d-d67c1e679521",
                            "first_name": "Fidella",
                            "last_name": "Yin",
                            "email": "fid@mail.com",
                            "role": "",
                            "created_at": "2023-12-14T10:27:00.350207Z",
                            "updated_at": "2023-12-14T14:58:56.734416Z",
                        },
                        {
                            "id": "42cb8405-581a-40c6-bd9c-5428a9dae49f",
                            "first_name": "Camey",
                            "last_name": "Fiifi",
                            "email": "cam@mail.com",
                            "role": "ADMIN",
                            "created_at": "2023-12-14T11:08:35.860506Z",
                            "updated_at": "2023-12-14T11:08:35.911617Z",
                        },
                        {
                            "id": "9ee19834-7310-4e5b-b68f-d96aac58172d",
                            "first_name": "Bernard",
                            "last_name": "Agyei",
                            "email": "ben@mail.com",
                            "role": "SUPER ADMIN",
                            "created_at": "2023-12-14T11:12:17.839982Z",
                            "updated_at": "2023-12-14T11:12:17.853010Z",
                        },
                        {
                            "id": "52cc7a8d-0887-4bc9-b17e-31f3c6170716",
                            "first_name": "Victor",
                            "last_name": "Ahumah",
                            "email": "kofiganoh@gmail.com",
                            "role": "",
                            "created_at": "2023-12-22T17:51:04.257995Z",
                            "updated_at": "2023-12-22T17:51:04.258013Z",
                        },
                    ]
                ),
                response_only=True,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        data = self.list(request, *args, **kwargs)
        response_data = CustomResponse.success(data=data)
        return Response(response_data)


class RetrieveDestroyUserView(RetrieveDestroyAPIView):
    permission_classes = [permissions.IsSuperAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def retrieve(self, request, pk, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset.get(pk=pk))
        return serializer.data

    @extend_schema(
        tags=["user"],
        description="Implements an endpoint to retrieve a user from the database",
        summary="Get a user from the database",
        responses={200: CustomUserSerializer},
        examples=[
            OpenApiExample(
                name="Example of a successful response after getting a user",
                value=CustomResponse.success(
                    data=[
                        {
                            "id": "0b0fd774-44fd-43ec-b9cf-51f055c97f00",
                            "first_name": "Kofi",
                            "last_name": "Ganoh",
                            "email": "kof@mail.com",
                            "role": "ADMIN",
                            "created_at": "2023-12-14T10:20:36.780216Z",
                            "updated_at": "2023-12-14T10:20:36.782908Z",
                        }
                    ]
                ),
                response_only=True,
            )
        ],
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            data = self.retrieve(request, pk)
            response_data = CustomResponse.success(data=data)
            return Response(response_data)
        except NotFound:
            error_response = CustomResponse.error(
                message="User does not exist", code=status.HTTP_404_NOT_FOUND
            )
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        tags=["user"],
        description="Implements an endpoint to delete a user from the database",
        summary="Delete a user",
        responses={200},
        examples=[
            OpenApiExample(
                name="Example of a successful deletion response",
                value=CustomResponse.success(),
                response_only=True,
            )
        ],
    )
    def delete(self, request, pk):
        self.destroy(request, pk)
        response_data = CustomResponse.success()
        return Response(response_data)
