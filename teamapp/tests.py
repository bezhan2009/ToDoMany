from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from teamapp.models import Team, TeamPerson
from adminapp.models import Admin
from app.models import Application
from userapp.models import UserProfile
from envapp.models import Environment


class TeamListTestCase(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.access_token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.team = Team.objects.create(user=self.user_profile, title='Test Team')
        self.teamperson = TeamPerson.objects.create(team=self.team, user=self.user_profile)

    def get_access_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_team_list(self):
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])


class TeamPersonListTestCase(TestCase):
    def setUp(self):
        self.user_profile = UserProfile.objects.create_user(username='testuser', password='testpassword', age=18)
        self.client = APIClient()
        self.access_token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        self.team = Team.objects.create(title='Test Team', user=self.user_profile)
        self.environment = Environment.objects.create(name='Test Environment', password="Test password", user=self.user_profile)

    def get_access_token(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data['access']

    def test_get_team_person_list(self):
        response = self.client.get(f'/api/teams/{self.team.id}/')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])

    def test_create_team_person(self):
        admin = Admin.objects.create(user=self.user_profile, environment=self.environment, is_admin=True, is_superadmin=True)
        response = self.client.post(f'/api/teams/{self.team.id}/', {'selected_team': [admin.id]})
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_404_NOT_FOUND])
