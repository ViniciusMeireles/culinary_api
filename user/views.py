from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipe.filters import RecipeChefFilter
from recipe.models import Recipe
from recipe.serializers import RecipeOfChefSerializer
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

    @extend_schema(
        responses={200: RecipeOfChefSerializer(many=True)},
        description=_('List recipes of a chef'),
    )
    @action(
        detail=True,
        methods=['get'],
        url_path='recipes',
        url_name='recipes',
        filterset_class=RecipeChefFilter,
        queryset=Recipe.objects.all(),
    )
    def list_recipes(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Recipe.objects.permitted_recipes(user=request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RecipeOfChefSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
