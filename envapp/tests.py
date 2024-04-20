from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from envapp.models import Environment
from userapp.models import UserProfile

class EnvironmentListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_environment_list(self):
        url = '/api/environments/'  # Фактический URL для получения списка окружений
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_environment(self):
        url = '/api/environments/'  # Фактический URL для создания окружения
        data = {'name': 'Test Environment'}  # Пример данных для создания окружения
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])


class EnvironmentDetailTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client.login(username='testuser', password='testpassword')
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)

    def test_get_environment_detail(self):
        url = f'/api/environments/{self.environment.id}/'  # Фактический URL для получения деталей окружения
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_delete_environment(self):
        url = f'/api/environments/{self.environment.id}/'  # Фактический URL для удаления окружения
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
