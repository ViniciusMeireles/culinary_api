from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from user.filters import ChefFilter
from user.models import Chef
from user.permissions import HisChefPermission
from user.serializers import ChefSerializer


@extend_schema_view(
    list=extend_schema(description=_('List chefs')),
    retrieve=extend_schema(description=_('Retrieve a chef')),
    create=extend_schema(description=_('Create a chef')),
    update=extend_schema(description=_('Update a chef')),
)
class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer
    permission_classes = [HisChefPermission]
    http_method_names = ['get', 'post', 'put']
    filterset_class = ChefFilter
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'
