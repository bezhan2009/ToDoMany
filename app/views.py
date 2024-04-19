from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from adminapp.models import Admin
from app.serializers import ApplicationQuerySerializer, ApplicationSerializer
from app.utils import ApplicationViewSet, ApplicationFun
from envapp.models import Environment
from userapp.models import UserProfile
from utils.tokens import get_user_id_from_token


# Create your views here.
class ApplicationActions(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        security=[],
        query_serializer=ApplicationQuerySerializer()
    )
    def get(self,
            request: Request,
            create_from_request: bool = False
            ) -> Response:
        query_serializer = ApplicationQuerySerializer(
            data=request.query_params
        )
        query_serializer.is_valid(
            raise_exception=True
        )

        get = query_serializer.validated_data.get("get", False)
        create = query_serializer.validated_data.get("create", False)
        delete = query_serializer.validated_data.get("delete", False)
        accept = query_serializer.validated_data.get("accept", False)
        application_pk = query_serializer.validated_data.get("application_pk")
        environment_pk = query_serializer.validated_data.get("environment_pk")
        accepted_funs = 0
        query_data = [get, create, delete, accept, create_from_request]

        accepted_funs = sum(query_data[:-1])

        if accepted_funs == 0:
            return Response(data={
                'message': 'No method is chose. Chooses are:',
                'methods': [
                    'get',
                    'create(post)',
                    'delete',
                    'accept'
                ]
            }, status=status.HTTP_400_BAD_REQUEST)
        elif accepted_funs > 1:
            return Response(data={
                'message': 'You cannot accept more than one method.',
                'methods': [
                    'get',
                    'create(post)',
                    'delete',
                    'accept'
                ]
            }, status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.get(id=get_user_id_from_token(request))
        if get:
            if not environment_pk:
                return Response(
                    data={'message': 'Environment has no provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            applicationfunc = ApplicationViewSet(
                environment_pk,
                get_user_id_from_token(request)
            )
            get_method = applicationfunc.get_application(request)

            if get_method == 403:
                return Response(
                    data={
                        'message': 'You have no permission to this action!!!'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            if get_method == 404:
                return Response(data={'message': 'Application Not Found'},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(get_method, status=status.HTTP_200_OK)

        elif create:
            if not environment_pk:
                return Response(
                    data={'message': 'Environment has no provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            applicationfunc = ApplicationViewSet(
                environment_pk,
                get_user_id_from_token(request)
            )
            create_method = applicationfunc.create_application(request)

            if create_method == 403:
                return Response(
                    data={
                        'message': 'You are already authorized to this env'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            if create_method == 'True':
                return Response(
                    data={
                        'message': 'The app has been successfully submitted'
                    },
                    status=status.HTTP_201_CREATED)
            elif create_method:
                return Response(
                    create_method,
                    status=status.HTTP_400_BAD_REQUEST)

        elif create_from_request:
            if not environment_pk:
                return Response(
                    data={'message': 'Environment has no provided.'},
                    status=status.HTTP_400_BAD_REQUEST)

            applicationfunc = ApplicationViewSet(
                environment_pk,
                get_user_id_from_token(request)
            )
            create_method = applicationfunc.create_application(request)

            if create_method == 'True':
                return create_method

            elif create_method:
                return Response(
                    create_method,
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif delete:
            if not application_pk:
                return Response(
                    data={'message': 'Application has no provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

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
                return Response(data={'message': 'Application Not Found.'},
                                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(
                    data={'message': 'You do not have access to this action'},
                    status=status.HTTP_403_FORBIDDEN
                )

        elif accept:
            if not application_pk:
                return Response(
                    data={'message': 'Application has no provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            applicationfunc = ApplicationFun(
                get_user_id_from_token(request),
                application_pk
            )
            accept_method = applicationfunc.accept_application(request)

            if accept_method == 404:
                return Response(
                    data={
                        'message': 'App not Found or has been deleted'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            elif accept_method:
                print(accept_method)
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
                    data={
                        'message': 'App has been successfully accepted'
                    },
                    status=status.HTTP_200_OK
                )
            elif not accept_method:
                return Response(
                    data={
                        'message': 'You do not have access to this action'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
