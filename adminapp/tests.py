from django.urls import reverse
from rest_framework.test import APITestCase
from userapp.models import UserProfile
from envapp.models import Environment
from .models import Admin


class AdminActionsViewTest(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)
        self.admin = Admin.objects.create(user=self.user, environment=self.environment)
    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, 200)
        return response.data['access']

    def test_get_tasks(self):
        url = reverse('adminapp:admin-actions', kwargs={'environment_pk': self.environment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_put_permissions(self):
        url = reverse('adminapp:admin-permissions', kwargs={'environment_pk': self.environment.id, 'admin_pk': self.admin.id})
        data = {'is_admin': True, 'is_superadmin': True}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)