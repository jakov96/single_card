from rest_framework.response import Response
from rest_framework.views import APIView
from route.manager import RouteManager


class GenerateRouteView(APIView):
    def get(self, request):
        place_count = int(self.request.query_params.get('place_count', 4))
        places = RouteManager.serialize(RouteManager.rand_select_places(place_count))

        return Response(places, status=200)
