from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from user.managers import ChefResponsibilityManager


class User(AbstractUser):
    pass


class ChefResponsibility(models.Model):
    class Types(models.TextChoices):
        EXECUTIVE_CHEF = "executive_chef", _("Executive Chef")
        CHEF = "chef", _("Chef")
        SOUS_CHEF = "sous_chef", _("Sous Chef")
        BAKER = "baker", _("Baker")
        PASTRY_CHEF = "pastry_chef", _("Pastry Chef")
        OTHER = "other", _("Other")

    label = models.CharField(
        verbose_name=_("Label of the Chef Type"),
        max_length=15,
        choices=Types.choices,
        unique=True,
    )

    objects = ChefResponsibilityManager()

    class Meta:
        verbose_name = _("Chef Responsibility")
        verbose_name_plural = _("Chef Responsibilities")

    def __str__(self):
        return self.label


class Chef(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.TextField(
        verbose_name=_("Biography"),
        blank=True,
        null=True,
        help_text=_("A brief description of the chef."),
    )
    responsibilities = models.ManyToManyField(
        ChefResponsibility,
        verbose_name=_("Responsibilities"),
        blank=True,
        help_text=_("The responsibilities of the chef."),
    )

    class Meta:
        verbose_name = _("Chef")
        verbose_name_plural = _("Chefs")
        ordering = ["-id"]

    def __str__(self):
        return self.user.username

    def set_responsibilities(self, *responsibility_labels):
        """
        Set the responsibilities of the chef.
        :param responsibility_labels: The labels of the ChefResponsibility objects.
        """
        self.responsibilities.set(ChefResponsibility.objects.filter_choices(*responsibility_labels))
