from rest_framework import viewsets, mixins
from core.models import PasswordPolicy
from password_policy import serializers
from . import permissions

class passwordPolicyViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    """manage password policy database"""

    queryset = PasswordPolicy.objects.all()
    serializer_class = serializers.PasswordPolicySerializer
    permission_classes = [permissions.PasswordPolicyPermission, ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """create new password policy"""
        serializer.save(user=self.request.user)

