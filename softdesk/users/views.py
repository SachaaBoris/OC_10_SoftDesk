"""
Users views
"""
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
)
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import (
    SignUpSerializer,
    UserSerializer,
)

class SignUp(generics.CreateAPIView):
    """Concrete view for creating a model instance of user object."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """A viewset that provides actions for user object."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class MyInfo(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Returns the object the view is displaying."""
        user = self.request.user

        # May raise a permission denied
        self.check_object_permissions(self.request, user)

        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        message = {
            "To delete your personal information": "send a mail with your email account at your administrator."
        }
        data = serializer.data
        data.update(message)
        return Response(data)

