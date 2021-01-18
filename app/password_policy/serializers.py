from rest_framework import serializers
from core.models import PasswordPolicy

class PasswordPolicySerializer(serializers.ModelSerializer):
    """serializers for password policy objects"""

    class Meta:
        model = PasswordPolicy
        fields = ('id', 'name', 'min_length', 'exp_interval',
                  'pwd_history', 'is_alpha_numeric', 'contains_username',
                  'must_mixed', 'status', 'last_updated', 'user')
        read_only_fields = ('id', 'user')


