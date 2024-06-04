from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from adminapp.models import Admin
from app.models import Application
from app.serializers import ApplicationSerializer
from envapp.models import Environment
from userapp.models import UserProfile
from utils.tokens import get_user_id_from_token
from .utils import ApplicationFun, ApplicationViewSet


class ApplicationList(APIView):
    def get(self, request: Request, environment_pk: int) -> Response:
        user = UserProfile.objects.get(id=get_user_id_from_token(request))
        applicationfunc = ApplicationViewSet(
            environment_pk,
            get_user_id_from_token(request)
        )
        get_method = applicationfunc.get_application(request)

        if get_method == 403:
            return Response(
                data={'message': 'You do not have permission for this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        elif get_method == 404:
            return Response(data={'message': 'Application not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(get_method, status=status.HTTP_200_OK)

    def post(self, request: Request, environment_pk: int) -> Response:
        user = UserProfile.objects.get(id=get_user_id_from_token(request))
        applicationfunc = ApplicationViewSet(
            environment_pk,
            get_user_id_from_token(request)
        )
        create_method = applicationfunc.create_application(request)

        if create_method == 403:
            return Response(
                data={'message': 'You are already authorized for this environment.'},
                status=status.HTTP_403_FORBIDDEN
            )
        elif create_method == 'True':
            return Response(
                data={'message': 'The app has been successfully submitted'},
                status=status.HTTP_201_CREATED)
        elif create_method:
            return Response(
                create_method,
                status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetails(APIView):
    def delete(self, request: Request, application_pk: int) -> Response:

        applicationfunc = ApplicationFun(
            get_user_id_from_token(request),
            application_pk)
        delete_method = applicationfunc.delete_application(request)

        if delete_method:
            return Response(
                data={'message': 'The app has been successfully removed'},
                status=status.HTTP_200_OK
            )
        elif delete_method == 404:
            return Response(data={'message': 'Application not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                data={'message': 'You do not have access to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

    def put(self, request: Request, application_pk: int) -> Response:

        applicationfunc = ApplicationFun(
            get_user_id_from_token(request),
            application_pk
        )
        accept_method = applicationfunc.accept_application(request)

        if accept_method == 404:
            return Response(
                data={'message': 'App not found or has been deleted'},
                status=status.HTTP_404_NOT_FOUND
            )
        elif accept_method:
            new_serializer = ApplicationSerializer(
                accept_method,
                many=False
            )
            accept_method = new_serializer

            user = UserProfile.objects.get(
                id=accept_method.data.get('user')
            )
            environment = Environment.objects.get(
                id=accept_method.data.get('environment')
            )
            admin = Admin.objects.create(user=user,
                                         environment=environment)
            admin.save()
            return Response(
                data={'message': 'App has been successfully accepted'},
                status=status.HTTP_200_OK
            )
        elif not accept_method:
            return Response(
                data={'message': 'You do not have access to this action'},
                status=status.HTTP_403_FORBIDDEN
            )
