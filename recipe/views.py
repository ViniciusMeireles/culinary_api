from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipe.models import Recipe
from recipe.pemissions import RecipePermission
from recipe.serializers import RecipeSerializer

from .filters import RecipeFilter


@extend_schema_view(
    list=extend_schema(description=_('List recipes')),
    retrieve=extend_schema(description=_('Retrieve a recipe')),
    create=extend_schema(description=_('Create a recipe')),
    update=extend_schema(description=_('Update a recipe')),
    destroy=extend_schema(description=_('Delete a recipe')),
)
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, RecipePermission]
    http_method_names = ['get', 'post', 'put', 'delete']
    filterset_class = RecipeFilter

    def get_queryset(self):
        # Shows public recipes, from the logged-in user and shared with the logged-in user
        return Recipe.objects.permitted_recipes(user=self.request.user)
