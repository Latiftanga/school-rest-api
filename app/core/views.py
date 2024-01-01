"""Views for the Core App"""
from rest_framework import (
    generics,
    authentication,
)
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from core import serializers
from core.permissions import IsUser


class CreateUserAccountView(generics.CreateAPIView):
    """Create a new teacher user account in the system"""

    serializer_class = serializers.UserAccountSerializer
    permission_classes = [AllowAny]


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    permission_classes = [AllowAny]


class ManageUserAccountView(generics.RetrieveUpdateAPIView):
    """Manage user account view"""
    serializer_class = serializers.UpdateUserAccountSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsUser]

    def get_object(self):
        """Retrieve the current authenticated user"""
        return self.request.user
