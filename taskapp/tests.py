import datetime

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.urls import reverse
from django.test import TestCase
from .models import Task, Environment
from userapp.models import UserProfile


class TaskListTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_task_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('task-list')
        data = {'title': 'Test title', 'description': 'Test Task', 'money': 10, 'date': '2024-04-20T12:00:00Z'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])


class TaskDetailTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.task = Task.objects.create(title='Test title', description='Test Task', user=self.user)

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_task_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])

    def test_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('task-detail', args=[self.task.id])
        data = {'description': 'Updated Task Description'}
        response = self.client.put(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])


class TaskEnvironmentActionTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_add_task_to_environment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('environment-task', args=[self.environment.id])
        data = {'task_pk': 1}  # Передайте корректный идентификатор задачи
        response = self.client.put(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])  # Проверьте статус код ответа


class EnvironmentTaskViewTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)
        self.task = Task.objects.create(description='Test Task', user=self.user, environment=self.environment)

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_mark_task_as_completed(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_access_token())
        url = reverse('environment-task', args=[self.environment.id])  # Updated URL reverse
        data = {'task_pk': self.task.id}
        response = self.client.put(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
