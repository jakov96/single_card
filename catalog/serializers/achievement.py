from rest_framework import serializers
from catalog.models import Achievement


class AchievementSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField(method_name='_logo')

    class Meta:
        model = Achievement
        fields = ('id', 'title', 'description', 'logo')

    def _logo(self, obj):
        return obj.get_logo()
