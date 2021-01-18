from rest_framework import viewsets, mixins
from core.models import PasswordPolicy
from password_policy import serializers

class passwordPolicyViewSet(viewsets.ModelViewSet, mixins.ListModelMixin):
    """manage password policy database"""

    queryset = PasswordPolicy.objects.all()
    serializer_class = serializers.PasswordPolicySerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)

