from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from organization.models import Organization
from organization.serializers.organization import OrganizationSerializer


class OrganizationListView(APIView):
    serializer_class = OrganizationSerializer

    def get(self, request):
        organizations = Organization.objects.all()
        serializer = self.serializer_class(organizations, many=True)

        return Response(serializer.data, status=200)


class OrganizationServiceList(APIView):
    serializer_class = OrganizationSerializer

    def get(self, request, organization_id):
        print(organization_id)
        organization = get_object_or_404(Organization, pk=organization_id)
        serializer = self.serializer_class(organization)
        return Response(serializer.data, status=200)
