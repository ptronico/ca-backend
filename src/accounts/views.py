from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from .permissions import IsObjectOwner
from .serializers import UserSerializer, UserLiteSerializer


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserLiteSerializer
    http_method_names = settings.REST_FRAMEWORK_ALLOWED_METHODS

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser | (permissions.IsAuthenticated & IsObjectOwner)]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        response = super().create(request, args, kwargs)
        user = User.objects.get(username=response.data['username'])
        response.data = UserSerializer(user, context={'request': request}).data
        return response

    def retrieve(self, request, username, *args, **kwargs):
        self.serializer_class = UserSerializer
        return super().retrieve(request, username, args, kwargs)
