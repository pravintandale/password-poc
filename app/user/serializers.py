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
        read_only_fields = ('id', )
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

    def validate_password(self, password):
        errors = dict()
        try:
            password_validation.validate_password(password=password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return password


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    policy_id = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password', 'policy_id')

    def validate_new_password(self, password):
        errors = dict()
        try:
            current_policy = self.context.get('user').password_policy.get(id=self.context.get('policy_id'))
            new_validators = [
                {
                    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
                    'OPTIONS': {'min_length': current_policy.min_length}
                },
                {
                    'NAME': 'user.validation.MinimumLowerCaseValidator',
                    'OPTIONS': {'min_lower': current_policy.min_lowercase}
                },
                {
                    'NAME': 'user.validation.MinimumUpperCaseValidator',
                    'OPTIONS': {'min_upper': current_policy.min_uppercase}
                },
                {
                    'NAME': 'user.validation.MinimumNumberValidator',
                    'OPTIONS': {'min_number': current_policy.min_number}
                },
                {
                    'NAME': 'user.validation.MinimumSpecialValidator',
                    'OPTIONS': {'min_special': current_policy.min_special_char}
                },
                {
                    'NAME': 'user.validation.MinimumDifferentValidator',
                    'OPTIONS': {'min_diff': current_policy.min_different_char}
                },
                {
                    'NAME': 'user.validation.UserAttributeSimilarityValidator',
                }
                # {
                #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
                # }
            ]
            if current_policy.max_consecutive_char:
                new_validators.append(
                    {
                        'NAME': 'user.validation.MaximumRepeatingValidator',
                        'OPTIONS': {'max_repeating': current_policy.max_consecutive_char}
                    }
                )
            if current_policy.max_consecutive_char_type:
                new_validators.append(
                    {
                        'NAME': 'user.validation.MaximumRepeatingTypeValidator',
                        'OPTIONS': {'max_repeating': current_policy.max_consecutive_char_type}
                    }
                )
            password_validation.validate_password(
                password=password,
                password_validators=password_validation.get_password_validators(new_validators)
            )
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return password
