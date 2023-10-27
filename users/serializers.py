from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "date_joined", "is_active", "is_staff", "password")

    def validate_email(self, value):
        value = value.lower()
        if get_user_model().objects.filter(email=value).exists():
            raise ValidationError("A user with this email address already exists.")
        return value
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class CustomUserSimpleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("name", "id")
    
    def get_name(self, obj):
        return obj.first_name + " " + obj.last_name
