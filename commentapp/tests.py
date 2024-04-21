import json
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from .models import Comment
from userapp.models import UserProfile
from taskapp.models import Task


class CommentListTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.access_token = self.get_access_token()
        self.task = Task.objects.create(user=self.user, title='test title', description='test description', money=10)

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_comments(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('comment-list', kwargs={'task_id': self.task.id})  # Use kwargs with the name of the argument from the URL pattern
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('comment-list', kwargs={'task_id': self.task.id})  # Use kwargs with the name of the argument from the URL pattern
        data = {'comment_text': 'Test comment text'}
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])


class CommentDetailTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.access_token = self.get_access_token()
        self.task = Task.objects.create(user=self.user, title='test title', description='test description', money=10)
        self.comment = Comment.objects.create(user=self.user, task_id=self.task.id, comment_text='Test comment text')

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_delete_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])
