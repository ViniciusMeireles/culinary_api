from django.db import models


class ChefResponsibilityManager(models.Manager):
    def all_choices(self):
        """Return a queryset of all ChefResponsibility objects."""
        list_of_create = list(set(self.model.Types.values) - set(self.model.objects.values_list("label", flat=True)))
        self.get_queryset().bulk_create(self.model(label=label) for label in list_of_create)
        return self.get_queryset().all()

    def filter_choices(self, *labels):
        """
        Return a queryset of ChefResponsibility objects for the given labels list.
        :param labels: The labels of the ChefResponsibility objects.
        """
        return self.all_choices().filter(label__in=labels)
