from typing import Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APITestCase

from user.models import Chef, ChefResponsibility

USER_MODEL = get_user_model()


def get_user_test_data(num: Optional[int] = 1, **kwargs):
    data = {
        'first_name': f'Test{num}',
        'last_name': f'User{num}',
        'password': f'test_password123*{num}',
        'email': f'usertest{num}@test.com',
        'username': f'user_test{num}',
    }
    data.update(kwargs)
    return data


def get_chef_test_data(num: Optional[int] = 1, **kwargs):
    data = {
        'bio': f'Test bio {num}',
    }
    data.update(**kwargs)
    return data


class BaseAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.chef = self.create_chef()
        self.user = self.chef.user

    def create_chef(self, num: Optional[int] = 1) -> Chef:
        user = USER_MODEL.objects.create_user(**get_user_test_data(num))
        chef = Chef.objects.create(**get_chef_test_data(num, user_id=user.id))
        chef.set_responsibilities(*ChefResponsibility.Types.values)
        return chef

    def authenticate_user(self, user: Optional[AbstractUser] = None):
        self.client.force_authenticate(user=user or self.user)
