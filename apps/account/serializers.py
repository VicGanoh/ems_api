from rest_framework import serializers
from django.contrib.auth.models

from apps.account.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            role=validated_data["role"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        """
        Validate the old_password, new_password and confirm_new_password fields.

        Args:
            attrs (dict): The dictionary containing the field values.

        Returns:
            dict: The validated attributes.

        Raises:
            serializers.ValidationError: If the passwords do not match.
        """
        old_password = data["old_password"]
        new_password = data["new_password"]
        confirm_new_password = data["confirm_new_password"]

        if new_password != confirm_new_password:
            return serializers.ValidationError("New password and confirm new password do not match")
        
        if not self.context["request"].user.check_password(old_password):
            return serializers.ValidationError("Old password is incorrect")
        
        return data
    
    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password", "confirm_new_password"]


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email"]
