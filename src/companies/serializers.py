from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='companies-detail', lookup_field='pk')

    class Meta:
        model = Company
        fields = ['id', 'name', 'url']


class CompanyLiteSerializer(CompanySerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'url']
