from django.conf import settings

from rest_framework import viewsets

from .models import Company
from .serializers import CompanySerializer
from .permissions import IsAdminOrReadOnly


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = settings.REST_FRAMEWORK_ALLOWED_METHODS
    permission_classes = [IsAdminOrReadOnly]
