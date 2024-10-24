from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class RecipeManager(models.Manager):
    def permitted_recipes(self, user: AbstractUser):
        """Shows public recipes, from the user and shared with the user."""
        return (
            self.get_queryset()
            .filter(
                Q(
                    is_public=True,
                    **(
                        {'chef__user_id': user.id, 'shared_with__user_id': user.id}
                        if user and user.is_authenticated
                        else {}
                    ),
                    _connector=Q.OR,
                )
            )
            .distinct()
        )
