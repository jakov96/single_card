from django.urls import path, re_path
from organization.views import OrganizationListView, OrganizationServiceList

urlpatterns = [
    path('', OrganizationListView.as_view(), name='organizations'),
    re_path(r'^(?P<organization_id>\d+)', OrganizationServiceList.as_view(), name='organization_services')
]
