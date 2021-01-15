from rest_framework import viewsets, mixins
from core.models import PasswordPolicy
from password_policy import serializers

class passwordPolicyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """manage password policy database"""

    queryset = PasswordPolicy.objects.all()
    serializer_class = serializers.PasswordPolicySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

