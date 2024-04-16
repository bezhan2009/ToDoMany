import logging

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken

from .funcs import (ApplicationViewSet,
                    ApplicationFun)
from .serializers import (UserProfileSerializer,
                          ApplicationQuerySerializer,
                          ApplicationSerializer,
                          TaskSerializer,
                          EnvironmentSerializer,
                          EnvironmentQuerySerializer,
                          SavedEnvironmentSerializer,
                          AdminEnvironmentSerializer,
                          CommentsSerializer,
                          TeamSerializer,
                          TeamQuerySerializer)
from ..models import (UserProfile,
                      Environment,
                      Admin,
                      Task,
                      SavedEnvironment,
                      Comment,
                      Team,
                      Application,
                      TeamPerson)

logger = logging.getLogger('django')


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER),
    }
))
@api_view(["POST"])
def create_user(request):
    """
    Создает нового пользователя.

    Свойства для создания нового пользователя:
    - username: Имя пользователя
    - password: Пароль
    - age: Возраст пользователя
    """
    data = {
        'username': request.data['username'],
        'password': request.data['password'],
        'age': request.data['age'],
    }
    serializer = UserProfileSerializer(data=data)

    if serializer.is_valid():
        user = serializer.create(serializer.validated_data)
        refresh = RefreshToken.for_user(user)
        logger.info(f"New user created with ID {user.id}.")

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user_id_from_token(request):
    try:
        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            access_token = AccessToken(authorization_header.split()[1])
            user_id = access_token['user_id']
            return user_id
        else:
            return
    except (AuthenticationFailed, IndexError):
        return


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


class TaskList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request):
        """
        Получает список задач пользователя.
        """
        user = UserProfile.objects.get(id=get_user_id_from_token(request))
        tasks = Task.objects.filter(user=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=TaskSerializer,
        responses={201: TaskSerializer()},
    )
    def post(self, request):
        """
        Создает новую задачу.
        """
        user_pk = get_user_id_from_token(request)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            user = UserProfile.objects.get(id=user_pk)
            serializer.save(user=user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TaskEnvironmentAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=TaskSerializer,
        responses={201: TaskSerializer()},
    )
    def post(self, request, pk):
        """
        Добавляет задачу в определенное окружение.
        """
        user_pk = get_user_id_from_token(request)
        task_user_pk = request.data.get('user')
        if not task_user_pk:
            return Response(data={'message': 'User has no provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=request.data)
        try:
            user = UserProfile.objects.get(id=user_pk)
            environment = Environment.objects.get(id=pk,
                                                  user=user)

        except Environment.DoesNotExist:
            try:
                environment = Environment.objects.get(id=pk)
            except Environment.DoesNotExist:
                return Response(data={'message': 'Environment not found'},
                                status=status.HTTP_404_NOT_FOUND)

            user = UserProfile.objects.filter(
                id=get_user_id_from_token(request)
            )
            admin = Admin.objects.filter(
                environment=environment,
                user=user
            )

            if not user.exists():
                return Response(data={'message': 'You Do Not Have access'},
                                status=status.HTTP_404_NOT_FOUND)
            elif not admin.exists():
                return Response(data={'message': 'You Do Not Have access'},
                                status=status.HTTP_404_NOT_FOUND)

        except UserProfile.DoesNotExist:
            return Response(
                data={'message': 'You have to chose one of the admins'},
                status=status.HTTP_404_NOT_FOUND
            )
        if serializer.is_valid():
            user = UserProfile.objects.get(id=task_user_pk)
            serializer.save(user=user,
                            environment=environment)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


class TaskDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, request):
        return get_object_or_404(
            Task,
            id=pk,
            user=UserProfile.objects.get(
                id=get_user_id_from_token(request)
            )
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={200: TaskSerializer()},
    )
    def get(self, request, pk):
        """
        Получает информацию о задаче.
        """
        try:
            task = self.get_object(pk, request)
        except Http404:
            return Response(
                data={'message': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={204: 'Task has been successfully removed'},
    )
    def delete(self, request, pk):
        """
        Удаляет задачу.
        """
        try:
            task = self.get_object(pk, request)
        except Http404:
            return Response(
                data={'message': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        task.is_deleted = True
        return Response(
            data={'message': 'Task has been successfully removed'},
            status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=TaskSerializer,
        responses={200: TaskSerializer()},
    )
    def put(self, request, pk):
        """
        Обновляет информацию о задаче.
        """
        try:
            task = self.get_object(pk, request)
        except Http404:
            return Response(
                data={'message': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)


class EnvironmentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={200: EnvironmentSerializer(many=True)},
    )
    def get(self, request):
        """
        Получает список всех сохраненных окружений.
        """
        try:
            user_id = get_user_id_from_token(request)
            environments = Environment.objects.filter(user=user_id)
        except Environment.DoesNotExist:
            return Response(
                data={
                    'message': 'You have not saved environments.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EnvironmentSerializer(environments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=EnvironmentSerializer,
        responses={
            201: 'Env has been successfully created',
            400: 'Env with this name is already taken. Please try again.'
        },
    )
    def post(self, request):
        """
        Создает новое окружение.
        """

        user_pk = get_user_id_from_token(request)
        serializer = EnvironmentSerializer(data=request.data)
        if serializer.is_valid():
            user = UserProfile.objects.get(id=user_pk)
            if Environment.objects.filter(
                    name=serializer.validated_data['name'],
                    user=user
            ):
                return Response(
                    data={
                        'message': 'Env with this name already exists'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(user=user)
            environment = Environment.objects.get(
                id=serializer.data.get('id')
            )
            saving_environment = SavedEnvironment.objects.create(
                user=user,
                environment=environment
            )
            saving_environment.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnvironmentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Environment, pk=pk, is_deleted=False)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={200: EnvironmentSerializer()},
        query_serializer=EnvironmentQuerySerializer()
    )
    def get(self, request, pk):
        """
        Получает информацию об определенном окружении.
        """

        query_serializer = EnvironmentQuerySerializer(
            data=request.query_params
        )
        query_serializer.is_valid(raise_exception=True)

        password = query_serializer.validated_data.get('password')
        try:
            environment = Environment.objects.filter(id=pk, is_deleted=False)
        except Environment.DoesNotExist:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not environment:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Получаем первичный ключ пользователя
        user_id = get_user_id_from_token(request)

        # Проверяем, существует ли запись для пользователя и окружения
        saved_environment_qs = SavedEnvironment.objects.filter(
            user=user_id,
            environment=pk
        )

        if saved_environment_qs.exists():
            # Если запись уже существует, обновляем ее дату
            saved_environment = saved_environment_qs.first()
            saved_environment.date = timezone.now()  # Обновляем дату
        else:
            # Если запись не существует, создаем новую запись
            if not password:
                return Response({'message': 'Password has no provided'})
            environment = Environment.objects.filter(id=pk)
            if environment.exists():
                environment = Environment.objects.filter(
                    id=pk,
                    password=password
                )
                if environment.exists():
                    data = {
                        'user': user_id,
                        'environment': pk,
                    }
                else:
                    return Response(
                        data={'message': 'Incorrect password'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            else:
                return Response(
                    data={'message': 'Environment Not Found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            saving_environment = SavedEnvironmentSerializer(data=data)
            if saving_environment.is_valid():
                saved_environment = saving_environment.save()
            else:
                return Response(
                    data=saving_environment.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        application = ApplicationActions()
        create_application = application.get(request, pk, True)
        print("Without If: ", create_application)
        if create_application == 'True':
            print("With If: ", create_application)
        else:
            print("With Else", create_application)
            return Response(
                data=create_application,
                status=status.HTTP_400_BAD_REQUEST
            )
        saved_environment.save()  # Сохраняем изменения или новую запись
        environment_instance = environment.first()
        serializer = EnvironmentSerializer(environment_instance, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="пароль от окружения для его удаления"
                ),
            },
            required=['password']
        ),
        responses={
            200: 'Environment has been removed successfully.',
            400: 'Password has no provided.',
            403: 'You do not have permission to delete this environment.',
            404: 'Environment not found',
        },
    )
    def delete(self, request, pk):
        """
        Удаляет окружение.
        """

        is_access = False
        try:
            password = request.data.get('password')
            if password:
                if Environment.objects.filter(
                        id=pk,
                        user=UserProfile.objects.get(
                            id=get_user_id_from_token(request)
                        )):
                    if Environment.objects.filter(id=pk, password=password):
                        is_access = True
                    else:
                        return Response(
                            data={'message': 'Incorrect password.'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                else:
                    pass
            else:
                return Response(
                    data={'message': 'Password has no provided.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            environment = self.get_object(pk)
        except Http404:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if is_access:
            environment.is_deleted = True
            environment.save()
        else:
            return Response(
                data={'message': 'You arent allowed to delete this env'},
                status=status.HTTP_403_FORBIDDEN)
        return Response(
            data={'message': 'Env has been removed successfully'},
            status=status.HTTP_200_OK
        )


class EnvironmentAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Environment,
                                 id=pk)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(
                id=get_user_id_from_token(request)
            )
            environment = Environment.objects.get(id=pk)
            admins = Admin.objects.filter(
                environment=environment)
        except Http404:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Environment.DoesNotExist:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if (Admin.objects.filter(
                environment=environment,
                user=user).exists() or
                Environment.objects.filter(
                    user=user).exists()):
            pass
        else:
            return Response(
                data={'message': 'You do not have access to this env'},
                status=status.HTTP_403_FORBIDDEN)
        if admins:
            serializer = AdminEnvironmentSerializer(admins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={'message': 'This env do not have any admins'},
                status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'admin_pk': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID администратора окружения"
                ),
            },
            required=['admin_pk']
        ),
        responses={201: 'You have successfully added your friend to env'},
    )
    def post(self, request, pk):
        """
        Добавляет пользователя в окружение в качестве администратора.
        """
        user_pk = get_user_id_from_token(request)
        user = UserProfile.objects.get(id=user_pk)
        is_access = False
        try:
            environment = self.get_object(pk)
        except Http404:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        admin_pk = request.data.get('admin_pk')
        if admin_pk is None:
            return Response(
                data={'message': 'admin_pk has no provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        environment_check = Environment.objects.filter(user=user)
        if environment_check:
            is_access = True
        elif Admin.objects.filter(user=user):
            is_access = True
        elif not is_access:
            return Response(
                data={'message': 'You arent allowed to add your friend'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            user_admin_pk = UserProfile.objects.get(id=admin_pk)
            admin = Admin.objects.filter(
                user=user_admin_pk,
                environment=environment
            ).first()
            if admin is None:
                if is_access:
                    admin = Admin.objects.create(
                        environment=environment,
                        user=UserProfile.objects.get(
                            id=admin_pk
                        )
                    )
                    if request.data.get('is_superadmin'):
                        admin.save(is_superadmin=True, is_admin=True)
                    return Response(
                        data={'message': 'You added your friend to env'},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        data={'message': 'You arent allowed to add friends'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            return Response(
                data={'message': 'This user is already admin in this env'},
                status=status.HTTP_200_OK
            )
        except UserProfile.DoesNotExist:
            return Response(
                data={'message': 'User does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                data={'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EnvironmentAdminAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user_pk, is_superadmin):
        if is_superadmin:
            return get_object_or_404(Environment,
                                     pk=pk, )
        else:
            return get_object_or_404(Environment,
                                     pk=pk,
                                     user=UserProfile.objects.get(id=user_pk))

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={200: 'Admin deleted successfully'},
    )
    def delete(self, request, pk, admin_pk):
        """
        Удаляет администратора из окружения.
        """
        user_pk = get_user_id_from_token(request)
        try:
            environment = self.get_object(pk, user_pk, False)
            is_access_to_delete_superadmin = True
        except Http404:
            try:
                environment = self.get_object(pk, user_pk, True)
                Admin.objects.get(
                    id=get_user_id_from_token(request),
                    is_superadmin=True,
                    environment=environment
                )
                is_access_to_delete_superadmin = False
            except Admin.DoesNotExist:
                return Response(
                    data={'message': 'You Do Not Have access.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            except Http404:
                return Response(
                    data={'message': 'Environment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if is_access_to_delete_superadmin:
            try:
                admin = Admin.objects.get(
                    id=admin_pk,
                    environment=environment
                )
            except Admin.DoesNotExist:
                return Response(
                    data={'message': 'Admin not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            try:
                admin = Admin.objects.get(
                    id=admin_pk,
                    is_superadmin=True,
                    environment=environment
                )
            except Admin.DoesNotExist:
                try:
                    admin = Admin.objects.get(
                        id=admin_pk,
                        environment=environment
                    )
                except Admin.DoesNotExist:
                    return Response(
                        data={'message': 'You do not have access'},
                        status=status.HTTP_403_FORBIDDEN
                    )
        admin.delete()
        return Response(
            data={'message': 'Admin deleted successfully'},
            status=status.HTTP_200_OK
        )


class AdminActionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request, environment_pk):
        """
        Получает список задач для текущего пользователя в указанном окружении.
        """

        is_admin = False
        try:
            environment = Environment.objects.get(id=environment_pk)
            admin = Admin.objects.filter(
                user=UserProfile.objects.get(
                    id=get_user_id_from_token(request)
                )
            )
        except Environment.DoesNotExist:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not admin.exists():
            if Environment.objects.filter(
                    id=environment_pk,
                    user=UserProfile.objects.get(
                        id=get_user_id_from_token(request)
                    )):
                is_admin = True
            else:
                return Response(
                    data={'message': 'You Do Not Have access'},
                    status=status.HTTP_404_NOT_FOUND
                )
        if is_admin:
            task = Task.objects.filter(environment=environment,
                                       is_deleted=False,
                                       completed=False)
        else:
            task = Task.objects.filter(environment=environment,
                                       user=UserProfile.objects.get(
                                           id=get_user_id_from_token(request)
                                       ),
                                       is_deleted=False,
                                       completed=False)

        if not task:
            return Response(
                data={'message': 'You have not any tasks.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TaskSerializer(task, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class EnvironmentTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_pk': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID задачи"
                ),
            },
            required=['task_pk']
        ),
        responses={200: 'Task has been completed'},
    )
    def put(self, request, environment_pk):
        """
        Помечает задачу в указанном окружении как завершенную.
        """
        user_pk = get_user_id_from_token(request)
        try:
            environment = Environment.objects.get(id=environment_pk,
                                                  user=UserProfile.objects.get(
                                                      id=user_pk)
                                                  )
        except Environment.DoesNotExist:
            try:
                environment = Environment.objects.get(id=environment_pk)
            except Environment.DoesNotExist:
                return Response(
                    data={'message': 'Environment not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            admin = Admin.objects.filter(environment=environment,
                                         user=UserProfile.objects.get(
                                             id=get_user_id_from_token(request)
                                         ),
                                         is_admin=True)
            if not admin.exists():
                return Response(
                    data={'message': 'You do not have access'},
                    status=status.HTTP_403_FORBIDDEN
                )
        task_pk = request.data.get('task_pk')
        try:
            task = Task.objects.get(environment=environment,
                                    id=task_pk)
        except Task.DoesNotExist:
            return Response(
                data={'message': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        task.completed = True
        return Response(
            data={'message': 'Task has been completed'},
            status=status.HTTP_200_OK
        )


def build_comment_tree(comment, comments_dict):
    comment_data = CommentsSerializer(instance=comment).data
    children_comments = comments_dict.get(comment.id, [])

    if children_comments:
        comment_data['children'] = [build_comment_tree(
            child,
            comments_dict
        ) for child in children_comments]

    return comment_data


class CommentList(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get_object(self, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            comments = Comment.objects.filter(task=task)
            comments_dict = {comment.id: [] for comment in comments}

            for comment in comments:
                if comment.parent_id:
                    comments_dict[comment.parent_id].append(comment)

            main_comments = [comment for comment in comments
                             if not comment.parent_id]

            return main_comments, comments_dict
        except Task.DoesNotExist:
            logger.warning("Failed to get comments. Task not found.")
            raise Response(
                data={"message": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            raise Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, task_id):
        try:
            main_comments, comments_dict = self.get_object(task_id)
            main_comments_tree = [build_comment_tree(
                comment,
                comments_dict
            ) for comment in main_comments]
            return Response(
                data=main_comments_tree,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'parent_id': openapi.Schema(
                    type=openapi.TYPE_NUMBER
                ),
                'comment_text': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
            },
            required=['comment_text']
        ),
        security=[],
    )
    def post(self, request, task_id):
        try:
            user_id = get_user_id_from_token(request)
            user_profile = UserProfile.objects.get(id=user_id)
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                parent_comment_id = request.data.get('parent_id')
                task = Task.objects.get(id=task_id)

                if parent_comment_id:
                    parent_comment = Comment.objects.get(id=parent_comment_id)
                    new_comment = serializer.save(
                        user=user_profile,
                        task=task)  # Сначала сохраняем новый комментарий

                    parent_comment.children.add(
                        new_comment
                    )
                else:
                    serializer.save(
                        user=user_profile,
                        task=task
                    )

                return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except UserProfile.DoesNotExist:
            logger.warning(
                "Failed to create a new comment. User profile not found."
            )
            return Response(
                data={"message": "You have not registered yet"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Task.DoesNotExist:
            logger.warning(
                "Failed to get comments. Task not found."
            )
            return Response(
                data={"message": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, _comment_id):
        try:
            return Comment.objects.get(id=_comment_id)
        except Comment.DoesNotExist:
            logger.warning(
                "Failed to get comments. Comment not found."
            )
            raise Http404({"message": "Comment not found"})
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            raise Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def delete_comment_chain(self, comment):
        # Recursively delete comment chain
        child_comments = Comment.objects.filter(parent_id=comment.id)
        for child_comment in child_comments:
            self.delete_comment_chain(child_comment)
            child_comment.delete()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        security=[],
    )
    def delete(self, request, comment_id):
        try:
            user_id = get_user_id_from_token(request)
            user_profile = UserProfile.objects.get(
                id=user_id
            )
            comment = Comment.objects.get(
                id=comment_id,
                user=user_profile
            )
            logger.info(
                "Attempting to delete comment with ID %s.",
                str(comment_id)
            )
        except Comment.DoesNotExist:
            logger.warning(
                "Failed to delete Comment. Comment with ID %s not found.",
                str(comment_id)
            )
            return Response(
                data={"message": "Comment Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Delete the entire comment chain
        self.delete_comment_chain(comment)

        # Delete the parent comment
        comment.delete()

        return Response(
            data={'message': 'comment has been successfully deleted!'},
            status=status.HTTP_200_OK
        )


class AdminPermissions(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'is_admin': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=False,
                    description='Is this user an admin?'),
                'is_superadmin': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=False,
                    description='Is this user a super admin?'),
            },
            required=['is_admin', 'is_superadmin']
        ),
        security=[],
    )
    def put(self, request, environment_pk, admin_pk):
        try:
            environment = Environment.objects.get(
                id=environment_pk
            )
        except Environment.DoesNotExist:
            return Response(
                data={'message': 'Environment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        admin = Admin.objects.filter(
            user__pk=get_user_id_from_token(request),
            is_superadmin=True
        )

        if admin.exists():
            is_permission_to_superedit = False
            is_permission_to_edit = True

        elif environment.user.id == get_user_id_from_token(request):
            is_permission_to_superedit = True
            is_permission_to_edit = True

        else:
            is_permission_to_superedit = False
            is_permission_to_edit = False

        if not is_permission_to_superedit and not is_permission_to_edit:
            return Response(
                data={'message': 'You have not permission to this action'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            admin = Admin.objects.get(id=admin_pk)
        except Admin.DoesNotExist:
            return Response(
                data={'message': 'Admin not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        is_superadmin = request.data.get('is_superadmin', False)
        is_admin = request.data.get('is_admin', False)

        admin_un = admin.user.username
        if is_permission_to_superedit:
            if is_superadmin and admin.is_superadmin:
                return Response(
                    data={'message': 'The admin is already a superadmin'},
                    status=status.HTTP_200_OK
                )

            elif is_superadmin and not admin.is_superadmin:
                admin.is_superadmin = True
                admin.is_admin = True
                admin.save()

                return Response(
                    data={
                        'message': f'User: {admin_un} became the superadmin'
                    },
                    status=status.HTTP_200_OK
                )

            elif is_admin and admin.is_admin:
                if admin.is_superadmin:
                    admin.is_superadmin = False
                    admin.save()
                    admin_un = admin.user.username
                    return Response(
                        data={'message': f'User: {admin_un} became the admin'},
                        status=status.HTTP_200_OK
                    )

                else:
                    return Response(
                        data={'message': 'The user is already an admin'},
                        status=status.HTTP_200_OK
                    )

            elif is_admin and not admin.is_admin:
                admin.is_admin = True
                admin.is_superadmin = False
                admin.save()
                return Response(
                    data={'message': f'User: {admin_un} became the admin'},
                    status=status.HTTP_200_OK
                )

            elif is_admin and admin.is_superadmin:
                admin.is_admin = True
                admin.is_superadmin = False
                admin.save()
                return Response(
                    data={'message': f'User: {admin_un} became the admin'},
                    status=status.HTTP_200_OK
                )

            elif not is_admin and not admin.is_admin:
                return Response(
                    data={'message': 'The user is already simple admin'},
                    status=status.HTTP_200_OK
                )

            elif not is_admin and not is_superadmin:
                if admin.is_admin:
                    admin.is_superadmin = False
                    admin.is_admin = False
                    admin.save()
                    return Response(
                        data={
                            'message': f'User: {admin_un} now is simple admin'
                        },
                        status=status.HTTP_200_OK
                    )

                else:
                    return Response(
                        data={'message': 'The admin is already simple admin'},
                        status=status.HTTP_200_OK
                    )

            else:
                return Response({'message': 'How can I help?'},
                                status=status.HTTP_400_BAD_REQUEST)

        elif is_permission_to_edit:
            if is_superadmin:
                return Response(
                    data={'message': 'You have not permission to this action'},
                    status=status.HTTP_403_FORBIDDEN
                )

            elif is_admin and admin.is_admin:
                return Response(
                    data={'message': 'The user is already an admin'},
                    status=status.HTTP_200_OK
                )

            elif is_admin and not admin.is_admin:
                admin.is_admin = True
                admin.save()
                return Response(
                    data={'message': f'User: {admin_un} became the admin'},
                    status=status.HTTP_200_OK
                )

            elif not is_admin and admin.is_admin:
                admin.is_admin = False
                admin.save()
                return Response(
                    data={
                        'message': f'User: {admin_un} now is simple admin'
                    },
                    status=status.HTTP_200_OK
                )

            elif not is_admin and not admin.is_admin:
                return Response(
                    data={'message': 'The user is already simple admin'},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    data={'message': 'How can I help?'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                data={'message': 'You have not permission to this action'},
                status=status.HTTP_403_FORBIDDEN
            )


class TeamList(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING
            ),
        ],
    )
    def get(self, request):
        user_id = get_user_id_from_token(request)
        user = UserProfile.objects.get(id=user_id)
        try:
            teams = Team.objects.filter(user=user)
        except Team.DoesNotExist:
            return Response({'message': 'You have not any teams yet.'})

        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
    )
    def post(self, request):
        user_id = get_user_id_from_token(request)
        user = UserProfile.objects.get(id=user_id)

        data = {
            'user': user
        }
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={'message': 'Team has been successfully created'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TeamPersonList(APIView):
    def get(self, request, team_pk):
        try:
            teams = Team.objects.filter(id=team_pk)
        except Team.DoesNotExist:
            return Response(
                data={'message': 'Team Not Found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeamSerializer(
            teams,
            many=True
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        query_serializer=TeamQuerySerializer(),
    )
    def post(self, request, team_pk=None):
        query_serializer = TeamQuerySerializer(
            data=request.query_params
        )
        query_serializer.is_valid(
            raise_exception=True
        )

        selected_team = query_serializer.validated_data.get('selected_team')

        try:
            if not selected_team:
                raise ValidationError("Please provide 'selected_team'")
        except ValidationError as V:
            return Response({'message': str(V)})
        user = UserProfile.objects.get(id=get_user_id_from_token(request))

        # Если не передан team_id, создаем новую команду
        try:
            team = get_object_or_404(Team, id=team_pk, user=user)
        except Http404:
            return Response(
                data={'message': 'Team not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        for admin_id in selected_team:
            selected_admin = get_object_or_404(
                Admin,
                id=admin_id,
                environment__user=user
            )
            if selected_admin.environment.user == user:
                TeamPerson.objects.get_or_create(
                    team=team,
                    user=selected_admin.user,
                    is_admin=selected_admin.is_admin,
                    is_superadmin=selected_admin.is_superadmin
                )
            else:
                application = Application.objects.create(
                    user=user,
                    to_user=selected_admin.user,
                    team=team)
                application.save()

        return Response(
            data={'message': 'Team created successfully'},
            status=status.HTTP_201_CREATED
        )
