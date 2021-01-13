from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')

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
