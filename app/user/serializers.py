from django.contrib.auth import get_user_model, password_validation
from django.core import exceptions
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    """serializer for users object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'company_name',
                  'country', 'require_password_change', 'preferred_language')
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, "write_only": True, }
        }

    def create(self, validated_data):
        """create a new user"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update User """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        errors = dict()
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)