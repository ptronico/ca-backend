from django.contrib.auth.models import User
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    api_token = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='users-detail', lookup_field='username')
    reviews_url = serializers.HyperlinkedIdentityField(view_name='users-reviews-list', lookup_field='username',
                                                       lookup_url_kwarg='username')

    class Meta:
        model = User
        fields = ['username', 'api_token', 'url', 'reviews_url']

    def get_api_token(self, obj):
        return obj.auth_token.key


class UserLiteSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username', 'url', 'reviews_url']

    def validate_username(self, value):
        """
        Ensure `value` contains only letter, numbers, underscores or hyphens.
        """
        try:
            validate_slug(value)
        except ValidationError:
            raise serializers.ValidationError('Username must have only letters, numbers, underscores or hyphens.')
        return value
