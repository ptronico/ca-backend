from rest_framework import serializers

from django.contrib.auth.models import User


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
        fields = ['username', 'url']
