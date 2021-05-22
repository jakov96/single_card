from django.urls import path
from route.views import GenerateRouteView

urlpatterns = [
    path('places/', GenerateRouteView.as_view(), name='generate_route'),

]
