from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from recipe.models import Recipe


class RecipeChefFilter(filters.FilterSet):
    """Recipe filter class."""

    servings = filters.NumberFilter(
        field_name='servings',
        lookup_expr='gte',
        label=_('Servings Greater Than'),
        help_text=_('Filter by servings greater than or equal to.'),
    )
    prep_time_lte = filters.DurationFilter(
        field_name='prep_time',
        lookup_expr='lte',
        label=_('Preparation Time Less Than'),
        help_text=_('Filter by preparation time less than or equal to.'),
    )
    prep_time_gte = filters.DurationFilter(
        field_name='prep_time',
        lookup_expr='gte',
        label=_('Preparation Time Greater Than'),
        help_text=_('Filter by preparation time greater than or equal to.'),
    )
    cook_time_lte = filters.DurationFilter(
        field_name='cook_time',
        lookup_expr='lte',
        label=_('Cook Time Less Than'),
        help_text=_('Filter by cooking time less than or equal to.'),
    )
    cook_time_gte = filters.DurationFilter(
        field_name='cook_time',
        lookup_expr='gte',
        label=_('Cook Time Greater Than'),
        help_text=_('Filter by cooking time greater than or equal to.'),
    )

    class Meta:
        model = Recipe
        fields = ['name', 'servings', 'prep_time_lte', 'prep_time_gte', 'cook_time_lte', 'cook_time_gte']


class RecipeFilter(RecipeChefFilter):
    """Recipe filter class with additional chef filter."""

    chef = filters.CharFilter(
        field_name='chef__user__username',
        label=_('Chef Username'),
        help_text=_('Filter by chef username.'),
    )

    class Meta:
        model = Recipe
        fields = ['name', 'chef', 'servings', 'prep_time_lte', 'prep_time_gte', 'cook_time_lte', 'cook_time_gte']
