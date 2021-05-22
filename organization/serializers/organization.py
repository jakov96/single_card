from rest_framework import serializers
from catalog.serializers.catalog import ServiceSerializer
from organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(source='get_services', many=True)

    class Meta:
        model = Organization
        fields = ('id', 'title', 'address', 'phone', 'services')

