from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from user.models import Chef, ChefResponsibility


class ChefFilter(filters.FilterSet):
    """Filter for chefs."""

    name = filters.CharFilter(
        label=_('Name'),
        help_text=_('Filter by chef name.'),
        method='filter_name',
    )
    has_recipes = filters.BooleanFilter(
        method='filter_has_recipes',
        label=_('Has Recipes'),
        help_text=_('Filter by chefs with recipes.'),
    )
    responsibilities = filters.ModelMultipleChoiceFilter(
        label=_('Responsibilities'),
        field_name='responsibilities__label',
        to_field_name='label',
        help_text=_('Filter by responsibilities.'),
        queryset=ChefResponsibility.objects.all(),
    )

    class Meta:
        model = Chef
        fields = ['name', 'responsibilities']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['responsibilities'].queryset = ChefResponsibility.objects.all_choices()

    def filter_has_recipes(self, queryset, name, value):
        if value is not None:
            queryset = queryset.exclude(recipes__isnull=value)
        return queryset

    def filter_name(self, queryset, name, value):
        if value:
            # Filter by first name or last name
            queryset = queryset.filter(
                Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value)
            ).distinct()
        return queryset
