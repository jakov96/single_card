from rest_framework import serializers
from catalog.models import Category, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('title', 'slug', 'is_free')


class CategorySerializer(serializers.ModelSerializer):
    services = ServiceSerializer(source='get_services', many=True)

    class Meta:
        model = Category
        fields = ('title', 'slug', 'services')


