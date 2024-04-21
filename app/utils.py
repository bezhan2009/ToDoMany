from django.utils import timezone

from adminapp.models import Admin
from app.models import Application
from app.serializers import ApplicationSerializer
from envapp.models import Environment


class ApplicationFun:
    """
    Contains the functions that are used in the ApplicationViewSet class.

    Attributes:
    user: The user that is trying to access the application.
    pk: The primary key of the application.
    """

    def __init__(self, user, pk):
        self.user = user
        self.pk = pk

    def delete_application(self, request: object) -> bool:
        """
        This function deletes the application
        If the user owns of the app or the admin of the env.
        """
        try:
            application = Application.objects.get(
                id=self.pk,
                is_deleted=False)
        except Application.DoesNotExist:
            return 404
        admin = Admin.objects.filter(environment=application.environment,
                                     user=self.user,
                                     is_admin=True)
        is_env_id = application.environment.user.id == self.user
        application_user = application.user.id == self.user
        if is_env_id or admin.exists() or application_user:
            is_accepted_for_delete = True
        else:
            is_accepted_for_delete = False
        if is_accepted_for_delete:
            application.is_deleted = True  # Исправлено на True
            application.save()
            return True
        return False

    def accept_application(self, request):
        """
        This function accepts the application
        """
        try:
            application = Application.objects.get(
                id=self.pk,
                is_accept=False,
                is_deleted=False)
        except Application.DoesNotExist:
            return 404

        admin = Admin.objects.filter(environment=application.environment,
                                     user=self.user,
                                     is_admin=True)
        if application.environment.user.id == self.user or admin.exists():
            application.is_accept = True
            application.save()
            return application
        return False


class ApplicationViewSet:
    """
    Contains the funcs that are used in the ApplicationViewSet.
    """

    def __init__(self, environment_pk, user):
        self.environment = environment_pk
        self.user = user

    def get_application(self, request):
        """
        This function gets the applications of the environment.
        """
        is_access = False
        environment = Environment.objects.get(id=self.environment)
        admin = Admin.objects.filter(user=self.user,
                                     environment=environment)
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
        """
        This function creates an application.
        """
        data = {
            'environment': self.environment,
            'user': self.user
        }
        application = Application.objects.filter(
            environment=self.environment,
            user=self.user
        )
        environment = Environment.objects.filter(
            id=self.environment,
            user=self.user
        )
        admin = Admin.objects.filter(
            user=self.user,
            environment=self.environment
        )
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