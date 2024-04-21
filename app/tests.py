from django.test import TestCase, Client
from rest_framework import status
from userapp.models import UserProfile
from .models import Application
from envapp.models import Environment
from app.views import ApplicationList, ApplicationDetails

class ApplicationListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.environment = Environment.objects.create(name='testenvironment', user=self.user, password='test password')
        self.application = Application.objects.create(
            user=UserProfile.objects.create_user(username='testuserforapplication',
                                                 password='testpasswordforapplication', age=18),
            environment=self.environment)

    def get_access_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        return response.data.get('access')

    def test_get_method(self):
        token = self.get_access_token()
        response = self.client.get(f'/api/application/{self.environment.id}/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method(self):
        token = self.get_access_token()
        response = self.client.post(f'/api/application/{self.environment.id}/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ApplicationDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.environment = Environment.objects.create(name='testenvironment', user=self.user, password='test password')
        self.application = Application.objects.create(
            user=UserProfile.objects.create_user(username='testuserforapplication',
                                                 password='testpasswordforapplication',
                                                 age=18), environment=self.environment)

    def get_access_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        return response.data.get('access')

    def test_delete_method(self):
        token = self.get_access_token()
        response = self.client.delete(f'/api/application/detail/{self.application.id}/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_method(self):
        token = self.get_access_token()
        response = self.client.put(f'/api/application/detail/{self.application.id}/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
