from rest_framework import status
from rest_framework.reverse import reverse_lazy

from common.tests import BaseAPITestCase, get_chef_test_data, get_user_test_data
from user.models import Chef, ChefResponsibility


class ChefAPITestCase(BaseAPITestCase):
    def test_list_chefs(self):
        """Test list chefs"""
        response = self.client.get(reverse_lazy('user:chefs-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), 1)

    def test_retrieve_chef(self):
        """Test retrieve chef"""
        response = self.client.get(reverse_lazy('user:chefs-detail', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.chef.id)

    def test_create_chef(self):
        """Test create chef"""
        data = get_user_test_data(2)
        data.update(get_chef_test_data(2), responsibilities=ChefResponsibility.Types.values)
        response = self.client.post(reverse_lazy('user:chefs-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chef.objects.count(), 2)

    def test_update_chef(self):
        """Test update chef"""
        self.authenticate_user()
        data = get_user_test_data(1)
        data.update(get_chef_test_data(2), responsibilities=ChefResponsibility.Types.values)

        response = self.client.put(
            reverse_lazy('user:chefs-detail', kwargs={'username': self.user.username}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.chef.refresh_from_db()
        self.assertEqual(self.chef.bio, data.get('bio'))
        self.assertEqual(self.user.first_name, data.get('first_name'))
