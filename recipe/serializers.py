from django.utils.translation import gettext as _
from rest_framework import serializers

from recipe.models import Recipe
from user.fields import ChefNameList
from user.models import Chef
from user.serializers import ChefSimpleSerializer


class RecipeSerializer(serializers.ModelSerializer):
    recipe_chef = ChefSimpleSerializer(
        source='chef', read_only=True, label=_('Chef'), help_text=_('Chef who created the recipe.')
    )
    shared_with = ChefNameList(
        label=_('Username List of Chefs'),
        help_text=_('List of chefs with whom the recipe is shared.'),
        required=False,
    )

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'description',
            'ingredients',
            'preparation_method',
            'recipe_chef',
            'servings',
            'prep_time',
            'cook_time',
            'is_public',
            'shared_with',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['shared_with'] = Chef.objects.filter(user__username__in=attrs.get('shared_with', [])).values_list(
            'id', flat=True
        )

        if (request := self.context.get('request')) and request.user.is_authenticated:
            try:
                attrs['chef_id'] = request.user.chef.id
            except Chef.DoesNotExist:
                raise serializers.ValidationError(_('You must be a chef to create a recipe.'))
            return attrs
        raise serializers.ValidationError(_('You must be authenticated to create a recipe.'))
