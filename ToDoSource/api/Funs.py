
from .serializers import *
from ToDoSource.models import *


class ApplicationFun:
    def __init__(self, user, pk):
        self.user = user
        self.pk = pk

    def delete_application(self, request):
        try:
            application = Application.objects.get(id=self.pk, is_deleted=False)
        except Application.DoesNotExist:
            return 404
        if (application.environment.user.id == self.user or Admin.objects.filter(environment=application.environment,
                                                                                 user=self.user,
                                                                                 is_admin=True).exists() or
                application.user == self.user):
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
            application = Application.objects.get(id=self.pk, is_accept=False, is_deleted=False)
        except Application.DoesNotExist:
            return 404

        if application.environment.user.id == self.user or Admin.objects.filter(environment=application.environment,
                                                                                user=self.user, is_admin=True).exists():
            application.is_accept = True
            application.save()
            return application
        else:
            return False


class ApplicationViewSet:
    def __init__(self, environment_pk, user):
        self.environment = environment_pk
        self.user = user

    def get_application(self, request):
        is_access = False
        admin = Admin.objects.filter(user=self.user, environment=Environment.objects.get(id=self.environment))
        if admin.exists():
            is_access = True
        else:
            environment = Environment.objects.filter(user=self.user)
            if environment.exists():
                is_access = True
        if not is_access:
            return 403
        applications = Application.objects.filter(environment=self.environment)
        serializer = ApplicationSerializer(applications, many=True)
        applications_data = serializer.data

        if not applications_data:
            return 404

        applications_accepts = {
            'accepted': [],
            'outcasts': []
        }

        for application in applications_data:
            if application['is_accept']:
                applications_accepts['accepted'].append(application)
            else:
                applications_accepts['outcasts'].append(application)

        return applications_accepts

    def create_application(self, request):
        data = {
            'environment': self.environment,
            'user': self.user
        }
        application = Application.objects.filter(environment=self.environment, user=self.user)
        environment = Environment.objects.filter(id=self.environment, user=self.user)
        admin = Admin.objects.filter(user=self.user, environment=self.environment)
        if environment.exists() or admin.exists():
            return 403
        if application.exists():
            application.data = timezone.now()
            return 'True'
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return 'True'
        return serializer.errors
