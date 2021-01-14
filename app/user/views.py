from django.contrib.auth import login, authenticate
from rest_framework import views, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

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


class LoginView(views.APIView):
    """Login view"""

    def post(self, request, format=None):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_active:
            login(request, user)
            return Response(data={"message": "login success"},
                            status=status.HTTP_200_OK)
        return Response(data={'message': 'Your account is currently deactivated.'},
                        status=status.HTTP_400_BAD_REQUEST)
