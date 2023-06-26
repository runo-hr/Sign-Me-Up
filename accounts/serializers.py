# accounts/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Add more fields as needed
        extra_kwargs = {
            'password': {'write_only': True}  # Hide password field in response
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
