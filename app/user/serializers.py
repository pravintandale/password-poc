from django.contrib.auth import get_user_model, password_validation, authenticate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'id')
        extra_kwargs = {
            'password': {"style": {"input_type": "password"}, "write_only": True, }
        }

    def create(self, validated_data):
        """create a new user"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer"""
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        print(email, password)
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
