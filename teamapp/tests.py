from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from teamapp.models import Team, TeamPerson
from adminapp.models import Admin
from app.models import Application
from userapp.models import UserProfile


class TeamListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')

    def test_get_team_list(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        response = self.client.post('/api/teams/')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])


class TeamPersonListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.team = Team.objects.create(name='Test Team', user=self.user)

    def test_get_team_person_list(self):
        response = self.client.get(f'/api/teams/{self.team.id}/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_create_team_person(self):
        admin = Admin.objects.create(user=self.user, environment=None, is_admin=True, is_superadmin=True)
        response = self.client.post(f'/api/teams/{self.team.id}/', {'selected_team': [admin.id]})
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_404_NOT_FOUND])

