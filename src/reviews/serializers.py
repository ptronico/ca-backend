from rest_framework import serializers

from accounts.serializers import UserLiteSerializer
from companies.serializers import CompanySerializer

from .models import Review
from .relations import HackedHyperlinkedIdentityField


class ReviewBaseSerializerMixin(object):
    def validate_rating(self, value):
        """
        Ensure `value` is in 1-5 range.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be greater or equal to 1 or less or equal to 5.")
        return value


class ReviewSerializer(ReviewBaseSerializerMixin, serializers.ModelSerializer):
    reviewer = UserLiteSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    url = HackedHyperlinkedIdentityField(view_name='users-reviews-detail', the_args=['reviewer.username', 'pk'])

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'company', 'title', 'summary', 'rating', 'ipv4', 'created', 'url']


class ReviewLiteSerializer(ReviewBaseSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['reviewer', 'company', 'title', 'summary', 'rating', 'ipv4']
