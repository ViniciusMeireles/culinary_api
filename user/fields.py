from rest_framework import fields

from user.models import ChefResponsibility
from user.validators import UsernameExistValidator


class ChefResponsibilityList(fields.ListField):
    """List of chef responsibilities in the form of a list of strings."""

    child = fields.ChoiceField(choices=ChefResponsibility.Types.choices)

    def to_representation(self, data):
        data = data.values_list('label', flat=True)
        return super().to_representation(data)


class ChefNameList(fields.ListField):
    """List of chef usernames in the form of a list of strings."""

    child = fields.CharField(validators=[UsernameExistValidator()])

    def to_representation(self, data):
        data = data.values_list('user__username', flat=True)
        return super().to_representation(data)
