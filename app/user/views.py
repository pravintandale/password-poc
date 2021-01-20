from django.contrib.auth import login, authenticate
from rest_framework import views, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from user import serializers, permissions
from core.models import User, PasswordPolicy


class UserViewSet(viewsets.ModelViewSet):
    """model view set for user"""
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.UserPermission, ]

    def get_queryset(self):
        qs = User.objects.all()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(email=self.request.user.email)

    @action(methods=('get',), detail=False)
    def me(self, request):
        serializer = self.get_serializer_class()(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        return {
            'view': self,
            'user': self.request.user
        }

    def perform_create(self, serializer):
        """Create user default policy"""
        user = serializer.save()
        PasswordPolicy.objects.create(name='Default', min_length=8, status=True, user=user)


class LoginView(ObtainAuthToken):
    """Login view"""

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check old password
        if not self.object.check_password(request.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        # Chek policy id belongs to user
        try:

            PasswordPolicy.objects.get(user=self.request.user, id=request.data.get('policy_id'))
        except PasswordPolicy.DoesNotExist:
            return Response({'ploicy_id': 'Does not belong to you.'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            # Set active policy.
            PasswordPolicy.objects.filter(user=self.request.user, status=True).update(status=False)
            PasswordPolicy.objects.filter(user=self.request.user, id=request.data.get('policy_id')).update(status=True)
            Token.objects.filter(user=self.request.user).delete()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully, please login again.',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        """Extra context provided to the serializer class."""
        return {
            'view': self,
            'user': self.request.user,
            'policy_id': self.request.data.get('policy_id')
        }
