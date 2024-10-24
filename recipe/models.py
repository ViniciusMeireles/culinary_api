from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from recipe.managers import RecipeManager


class Recipe(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Name"), help_text=_("The name of the recipe."))
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description of the recipe."),
        blank=True,
        null=True,
    )
    ingredients = models.TextField(verbose_name=_("Ingredients"), help_text=_("Ingredients of the recipe"))
    preparation_method = models.TextField(
        verbose_name=_("Preparation Method"),
        help_text=_("Preparation method of the recipe"),
    )
    chef = models.ForeignKey(
        to="user.Chef",
        on_delete=models.CASCADE,
        verbose_name=_("Chef"),
        help_text=_("The chef of the recipe."),
        related_name="recipes",
    )
    servings = models.IntegerField(
        verbose_name=_("Servings"),
        help_text=_("Servings of the recipe"),
        default=1,
        validators=[MinValueValidator(limit_value=1, message=_("Servings must be equal to or greater than 1."))],
    )
    prep_time = models.DurationField(
        verbose_name=_("Prep Time"),
        help_text=_("Preparation time of the recipe"),
        validators=[
            MinValueValidator(
                limit_value=timezone.timedelta(minutes=1),
                message=_("Preparation time must be equal to or greater than 1 minute."),
            ),
        ],
    )
    cook_time = models.DurationField(
        verbose_name=_("Cook Time"),
        help_text=_("Cooking time of the recipe"),
        validators=[
            MinValueValidator(
                limit_value=timezone.timedelta(minutes=0),
                message=_("Cooking time must be equal to or greater than 0 minutes."),
            )
        ],
        blank=True,
        null=True,
    )
    is_public = models.BooleanField(
        verbose_name=_("Is Public"),
        help_text=_("Whether the recipe is public or not."),
        default=False,
    )
    shared_with = models.ManyToManyField(
        to="user.Chef",
        verbose_name=_("Shared With"),
        help_text=_("Chefs with whom the recipe is shared."),
        related_name="shared_recipes",
        blank=True,
    )

    objects = RecipeManager()

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
        ordering = ["-id"]

    def __str__(self):
        return self.name
