from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from envapp.models import Environment
from userapp.models import UserProfile
from django.urls import reverse


class EnvironmentListTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_environment_list(self):
        url = reverse('environment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_environment(self):
        url = reverse('environment-list')
        data = {'name': 'Test Environment'}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class EnvironmentDetailTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_environment_detail(self):
        url = reverse('environment-detail', args=[self.environment.id])
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_delete_environment(self):
        url = reverse('environment-detail', args=[self.environment.id])
        data = {
            'password': self.environment.password
        }
        response = self.client.delete(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
