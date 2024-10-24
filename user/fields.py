from rest_framework import fields

from user.models import ChefResponsibility
from user.validators import UsernameExistValidator


class ChefResponsibilityList(fields.ListField):
    child = fields.ChoiceField(choices=ChefResponsibility.Types.choices)

    def to_representation(self, data):
        data = data.values_list('label', flat=True)
        return super().to_representation(data)


class ChefNameList(fields.ListField):
    child = fields.CharField(validators=[UsernameExistValidator()])

    def to_representation(self, data):
        data = data.values_list('user__username', flat=True)
        return super().to_representation(data)
