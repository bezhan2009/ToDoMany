from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.views import Response
from rest_framework import status
from .views import ApplicationList, ApplicationDetails


class ApplicationListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_get_method(self):
        request = self.factory.get('/api/applications/19/')
        response = ApplicationList.as_view()(request, environment_pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method(self):
        request = self.factory.post('/api/applications/19/')
        response = ApplicationList.as_view()(request, environment_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ApplicationDetailsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_delete_method(self):
        request = self.factory.delete('/api/applications/details/1/')
        response = ApplicationDetails.as_view()(request, application_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_method(self):
        request = self.factory.put('/api/applications/details/1/')
        response = ApplicationDetails.as_view()(request, application_pk=1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
