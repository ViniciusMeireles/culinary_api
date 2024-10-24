from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from user.models import User


@deconstructible
class UsernameExistValidator(BaseValidator):
    message = _('User not found.')

    def __init__(self, message=None):
        super().__init__(limit_value=None, message=message)

    def __call__(self, value):
        self.clean(value)

    def clean(self, value):
        if not (user := User.objects.filter(username=value).first()):
            raise ValidationError(self.message)
        return user.id
