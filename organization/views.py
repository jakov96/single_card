from rest_framework.response import Response
from rest_framework.views import APIView
from organization.models import Organization
from organization.serializers.organization import OrganizationSerializer


class OrganizationListView(APIView):
    serializer_class = OrganizationSerializer

    def get(self, request):
        organizations = Organization.objects.filter(is_confirm=True)
        serializer = self.serializer_class(organizations, many=True)

        return Response(serializer.data, status=200)


class OrganizationServiceList(APIView):
    serializer_class = OrganizationSerializer

    def get(self, request, organization_id):
        organization = Organization.objects.filter(id=organization_id, is_confirm=True).first()
        if organization:
            serializer = self.serializer_class(organization)
            return Response(serializer.data, status=200)
        return Response({
            'message': 'organization not found'
        }, status=404)
