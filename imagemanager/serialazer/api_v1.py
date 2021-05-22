from rest_framework import serializers
from imagemanager.models import BaseImage


class BaseImageSerializer(serializers.ModelSerializer):
    image_min = serializers.CharField(source='get_image_min_url', read_only=True)
    image_middle = serializers.CharField(source='get_image_middle_url', read_only=True)
    image_large = serializers.CharField(source='get_image_large_url', read_only=True)

    class Meta:
        model = BaseImage
        fields = ('id', 'original', 'image_min', 'image_middle', 'image_large', 'alt', 'width', 'height')
