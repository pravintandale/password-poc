from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):

    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user