import json

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Category, Achievement
from catalog.serializers.achievement import AchievementSerializer
from catalog.serializers.catalog import CategorySerializer


class CategoryListView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)

        return Response(serializer.data, status=200)


class AchievementListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AchievementSerializer

    def get(self, request):
        if self.request.user.is_authenticated:
            user_achievements = self.request.user.achievements.all()
            all_achievements = Achievement.objects.exclude(id__in=user_achievements)

            return Response({
                'received': self.serializer_class(user_achievements, many=True).data,
                'not_received': self.serializer_class(all_achievements, many=True).data
            }, status=200)

        return Response({'success': False}, status=401)
