from datetime import timedelta
from typing import Optional

from django.utils.dateparse import parse_duration
from django.utils.duration import duration_string
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from common.tests import BaseAPITestCase
from recipe.models import Recipe


def get_recipe_test_data(num: Optional[int] = 1, is_time_str_format: Optional[bool] = False, **kwargs):
    prep_time = timedelta(hours=num)
    cook_time = timedelta(hours=num)
    if is_time_str_format:
        prep_time = duration_string(prep_time)
        cook_time = duration_string(cook_time)
    data = {
        'name': f'Test Recipe {num}',
        'description': f'Test description {num}',
        'ingredients': f'Test ingredients {num}',
        'preparation_method': f'Test preparation method {num}',
        'servings': num,
        'prep_time': prep_time,
        'cook_time': cook_time,
        'is_public': True,
    }
    data.update(kwargs)
    return data


class RecipeAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.recipe = self.create_recipe()

    def create_recipe(self, num: Optional[int] = 1, chef_id: Optional[int] = None, **kwargs):
        if not chef_id:
            chef_id = self.chef.id
        data = get_recipe_test_data(num, chef_id=chef_id, **kwargs)
        return Recipe.objects.create(**data)

    def test_list_recipes(self):
        """Test list recipes"""
        response = self.client.get(reverse_lazy('recipe:recipes-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), 1)

    def test_retrieve_recipe(self):
        """Test retrieve recipe"""
        response = self.client.get(reverse_lazy('recipe:recipes-detail', kwargs={'pk': self.recipe.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.recipe.id)

    def test_create_recipe(self):
        """Test create recipe"""
        self.authenticate_user()
        other_chef = self.create_chef(num=2)
        data = get_recipe_test_data(num=2, is_time_str_format=True, shared_with=[other_chef.user.username])

        response = self.client.post(reverse_lazy('recipe:recipes-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 2)

    def test_update_recipe(self):
        """Test update recipe"""
        self.authenticate_user()
        other_chef = self.create_chef(num=2)
        data = get_recipe_test_data(1, is_time_str_format=True, shared_with=[other_chef.user.username])

        response = self.client.put(reverse_lazy('recipe:recipes-detail', kwargs={'pk': self.recipe.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.name, data.get('name'))
        self.assertEqual(self.recipe.description, data.get('description'))
        self.assertEqual(self.recipe.ingredients, data.get('ingredients'))
        self.assertEqual(self.recipe.preparation_method, data.get('preparation_method'))
        self.assertEqual(self.recipe.servings, data.get('servings'))
        self.assertEqual(self.recipe.prep_time, parse_duration(data.get('prep_time')))
        self.assertEqual(self.recipe.cook_time, parse_duration(data.get('cook_time')))
        self.assertEqual(self.recipe.is_public, data.get('is_public'))
        self.assertEqual(self.recipe.chef_id, self.chef.id)
        self.assertEqual(self.recipe.shared_with.count(), 1)

    def test_delete_recipe(self):
        """Test delete recipe"""
        self.authenticate_user()
        response = self.client.delete(reverse_lazy('recipe:recipes-detail', kwargs={'pk': self.recipe.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)
