from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.views import Response
from rest_framework import status
from django.contrib.auth.models import User  # Импорт модели пользователя
from .views import ApplicationList, ApplicationDetails
from userapp.models import UserProfile


class ApplicationListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)

    def test_get_method(self):
        # Использование тестового пользователя при отправке запроса
        request = self.factory.get('/api/applications/19/')
        request.user = self.user  # Установка тестового пользователя в запросе
        response = ApplicationList.as_view()(request, environment_pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method(self):
        # Использование тестового пользователя при отправке запроса
        request = self.factory.post('/api/applications/19/')
        request.user = self.user  # Установка тестового пользователя в запросе
        response = ApplicationList.as_view()(request, environment_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ApplicationDetailsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        # Создание тестового пользователя с моделью UserProfile
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)

    def test_delete_method(self):
        # Использование тестового пользователя при отправке запроса
        request = self.factory.delete('/api/applications/details/1/')
        request.user = self.user  # Установка тестового пользователя в запросе
        response = ApplicationDetails.as_view()(request, application_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_method(self):
        # Использование тестового пользователя при отправке запроса
        request = self.factory.put('/api/applications/details/1/')
        request.user = self.user  # Установка тестового пользователя в запросе
        response = ApplicationDetails.as_view()(request, application_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
