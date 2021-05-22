from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models import Category
from catalog.serializers.catalog import CategorySerializer


class CategoryListView(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)

        return Response(serializer.data, status=200)
