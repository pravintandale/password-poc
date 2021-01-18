from rest_framework import viewsets, mixins
from core.models import PasswordPolicy
from password_policy import serializers
from user import permissions

class passwordPolicyViewSet(viewsets.ModelViewSet):
    """manage password policy database"""

    queryset = PasswordPolicy.objects.all()
    serializer_class = serializers.PasswordPolicySerializer
    permission_classes = [permissions.UserPermission, ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """create new password policy"""
        if serializer.validated_data.get('status'):
            PasswordPolicy.objects.filter(user=self.request.user).update(status=False)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """update password policy"""
        if serializer.validated_data.get('status'):
            PasswordPolicy.objects.filter(user=self.request.user).update(status=False)
        serializer.save()

