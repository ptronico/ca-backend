from rest_framework import viewsets

from .models import Company
from .serializers import CompanySerializer
from .permissions import IsAdminOrReadOnly


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
