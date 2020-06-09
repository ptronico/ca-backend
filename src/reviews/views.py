from rest_framework import exceptions, generics, response, permissions

from django.contrib.auth.models import User

from companies.models import Company
from accounts.permissions import IsObjectOwner

from .models import Review
from .serializers import ReviewSerializer, ReviewLiteSerializer


class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAdminUser | (permissions.IsAuthenticated & IsObjectOwner)]

    def get_queryset(self):
        """
        Filter reviews by owner.
        """
        return Review.objects.filter(reviewer__username=self.kwargs['username'])

    def create(self, request, *args, **kwargs):
        """
        Custom create method using `ReviewLiteSerializer`.
        """
        company = Company.objects.get(id=request.data['company_id'])
        reviewer = User.objects.get(username=self.kwargs['username'])

        data = {
            'company': company.pk,
            'reviewer': reviewer.pk,
            'title': request.data.get('title', ''),
            'summary': request.data.get('summary', ''),
            'rating': request.data.get('rating', ''),
            'ipv4': request.META.get('REMOTE_ADDR', ''),
        }

        serializer = ReviewLiteSerializer(data=data)
        if serializer.is_valid():
            review = serializer.save()

            data = ReviewSerializer(review, context={'request': request}).data
            resp = response.Response(data)
            resp.status_code = 201
            return resp

        raise exceptions.ValidationError()


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAdminUser | (permissions.IsAuthenticated & IsObjectOwner)]

    def get_queryset(self):
        return Review.objects.filter(reviewer__username=self.kwargs['username'])

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, args, kwargs)
