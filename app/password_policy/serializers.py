from rest_framework import serializers
from core.models import PasswordPolicy

class PasswordPolicySerializer(serializers.ModelSerializer):
    """serializers for password policy objects"""

    class Meta:
        model = PasswordPolicy
        fields = ('name', 'user')
        read_only_fields = ('id',)


