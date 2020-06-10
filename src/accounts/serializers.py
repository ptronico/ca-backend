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
    username = serializers.CharField(min_length=3, max_length=User.username.field.max_length)

    class Meta:
        model = User
        fields = ['username', 'url', 'reviews_url']

    def validate_username(self, value):
        """
        Ensure `value` contains only letter, numbers, underscores or hyphens and is unique username.
        """
        try:
            validate_slug(value)
        except ValidationError:
            raise serializers.ValidationError('Username must have only letters, numbers, underscores or hyphens.')

        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            user = None

        if user:
            raise serializers.ValidationError('A user with that username already exists.')

        return value
