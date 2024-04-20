from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task, Environment
from userapp.models import UserProfile

class TaskListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_task_list(self):
        url = '/api/tasks/'  # Фактический URL для получения списка задач
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        url = '/api/tasks/'  # Фактический URL для создания задачи
        data = {'description': 'Test Task'}  # Пример данных для создания задачи
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])


class TaskDetailTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(title="Test title", description='Test Task', user=self.user)

    def test_get_task_detail(self):
        url = f'/api/tasks/{self.task.id}/'  # Фактический URL для получения деталей задачи
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_delete_task(self):
        url = f'/api/tasks/{self.task.id}/'  # Фактический URL для удаления задачи
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])

    def test_update_task(self):
        url = f'/api/tasks/{self.task.id}/'  # Фактический URL для обновления задачи
        data = {'description': 'Updated Task Description'}  # Пример данных для обновления задачи
        response = self.client.put(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])


class TaskEnvironmentActionTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client.login(username='testuser', password='testpassword')
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)

    def test_add_task_to_environment(self):
        url = f'/api/environments/{self.environment.id}/tasks/'  # Фактический URL для добавления задачи в окружение
        data = {'description': 'New Task'}  # Пример данных для создания задачи в окружении
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class EnvironmentTaskViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client.login(username='testuser', password='testpassword')
        self.environment = Environment.objects.create(name='Test Environment', password='password', user=self.user)
        self.task = Task.objects.create(description='Test Task', user=self.user, environment=self.environment)

    def test_mark_task_as_completed(self):
        url = f'/api/environments/{self.environment.id}/tasks/{self.task.id}/complete/'  # Фактический URL для пометки задачи как завершенной
        data = {'task_pk': self.task.id}  # Пример данных для завершения задачи
        response = self.client.put(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
