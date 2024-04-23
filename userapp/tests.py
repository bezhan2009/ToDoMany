from django.test import TestCase

from .models import User


# Create your tests here.
class TestAuth(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_creation(self):
        # Check if the user was created
        self.assertEqual(self.user.username, 'testuser')

    def test_user_creation_fail(self):
        # Check if the user was created
        self.assertNotEqual(self.user.username, 'testuser1')

    def test_login(self):
        # Check if the user can log in
        response = self.client.post('/auth/sign-in/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_fail(self):
        # Check if the user can log in
        response = self.client.post('/auth/sign-in/', {
            'username': 'testuser',
            'password': 'testpassword1'
        })
        self.assertEqual(response.status_code, 401)


class TestTokens(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        response = self.client.post('/auth/sign-in/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_token_creation(self):
        # Check if the token is created
        response = self.client.post('/auth/sign-in/', {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_creation_fail(self):
        # Check if the token is created
        response = self.client.post('/auth/sign-in/', {
            'username': 'testuser',
            'password': 'testpassword1'
        })
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_token_refresh(self):
        # Check if the token is refreshed
        response = self.client.post('/auth/token/refresh/', {
            'refresh': self.refresh_token
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_token_refresh_fail(self):
        # Check if the token is refreshed
        response = self.client.post('/auth/token/refresh/', {
            'refresh': self.refresh_token + '1'
        })
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
