from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from ToDoSource.models import *


class ApplicationFun:
    def __init__(self, environment, user, pk):
        self.environment = environment
        self.user = user
        self.pk = pk

    def get_application(self, request):
        applications = Application.objects.filter(environment=Environment.objects.get(id=pk))
        if applications.exists():
            return 404

        applications_accepts = {
            'accepted': None,
            'outcasts': None
        }
        for application in applications:
            if application.is_accept:
                applications['accepted'].append(application)
            else:
                applications['outcasts'].append(application)

        return Response(applications_accepts, status=status.HTTP_200_OK)

    def create_application(self, request):
        data = {
            'environment': self.environment,
            'user': self.user
        }
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return 'True'
        return serializer.errors

    def delete_application(self, request):
        try:
            application = Application.objects.get(id=self.pk)
        except Application.DoesNotExist:
            return "Application Not Found"
        if self.environment.user == self.user or Admin.objects.filter(environment=self.environment, user=self.user, is_admin=True).exists() or application.user == self.user:
            is_accepted_for_delete = True
        else:
            is_accepted_for_delete = False
        if is_accepted_for_delete:
            application.is_deleted = False
            application.save()
            return True
        else:
            return False

    def accept_application(self, request):
        try:
            application = Application.objects.get(id=self.pk)
        except Application.DoesNotExist:
            return 404

        if self.environment.user == self.user or Admin.objects.filter(environment=self.environment, user=self.user, is_admin=True).exists():
            application.is_accepted = True
            application.save()
            return True
        else:
            return False
