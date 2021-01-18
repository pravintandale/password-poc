from rest_framework import serializers
from core.models import PasswordPolicy

class PasswordPolicySerializer(serializers.ModelSerializer):
    """serializers for password policy objects"""

    class Meta:
        model = PasswordPolicy
        fields = ('name', 'min_length', 'min_characters', 'min_lowercase', 'min_uppercase', 'min_special_char',
                  'min_different_char', 'max_consecutive_char', 'max_consecutive_char_type', 'exp_interval',
                  'warn_interval', 'pwd_history', 'is_alpha_numeric', 'allow_username')
        read_only_fields = ('id', 'user')


