from rest_framework import serializers
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
        old_password = data.get("old_password")
        
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Context missing 'request'")
        
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")
        
        return data
    
    def update(self, instance, validated_data):
        new_password = validated_data["new_password"]
        instance.set_password(new_password)
        instance.save()
        return instance
    
    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password", "confirm_new_password"]


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get("email")
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with provided email does not exist")
        
        return attrs


