from django.urls import reverse
from rest_framework.test import APITestCase


class AdminActionsViewTest(APITestCase):
    def test_get_tasks(self):
        url = reverse('adminapp:admin-actions', kwargs={'environment_pk': 19})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_put_permissions(self):
        url = reverse('adminapp:admin-permissions', kwargs={'environment_pk': 19, 'admin_pk': 1})
        data = {'is_admin': True, 'is_superadmin': True}  # Пример данных для запроса
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
