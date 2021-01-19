from django.contrib.auth import login, authenticate
from rest_framework import views, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from user import serializers, permissions
from core.models import User


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
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

