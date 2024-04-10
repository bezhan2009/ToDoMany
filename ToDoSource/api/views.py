from django.shortcuts import get_object_or_404
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from django.db import transaction
from Funs import ApplicationFun
from .serializers import *
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
import logging
from django.db.models import Q
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

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
        user = UserProfile.objects.create_user(**data)
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
            return None
    except (AuthenticationFailed, IndexError):
        return None


class ApplicationActions(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        security=[],
        query_serializer=ApplicationQuerySerializer()
    )
    def get(self, request, pk, create_from_request=False):
        query_serializer = ApplicationQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        get = query_serializer.validated_data.get("Get", False)
        create = query_serializer.validated_data.get("Create", False)
        delete = query_serializer.validated_data.get("Delete", False)
        accept = query_serializer.validated_data.get("Accept", False)

        accepted_funs = 0
        query_data = [get, create, delete, accept, create_from_request]

        for q in query_data:
            if q:
                accepted_funs += 1

        if accepted_funs > 1:
            return Response({'message': 'You cannot accept more than one method\nChooses are:\n\tget\n\tcreate(post)\n\tdelete\n\taccept'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            environment = Environment.objects.get(id=pk)
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        user = UserProfile.objects.get(id=get_user_id_from_token(request))
        applicationfun = ApplicationFun(environment, user, pk)
        if get:
            get_method = applicationfun.get_application(request)
            return Response(get_method)
        elif create:
            create_method = applicationfun.create_application(request)
            if create_method == 'True':
                return Response({'message': 'The application has been successfully submitted'},
                                status=status.HTTP_201_CREATED)
            elif create_method:
                return Response(create_method, status=status.HTTP_400_BAD_REQUEST)
        elif create_from_request:
            create_method = applicationfun.create_application(request)
            if create_method == 'True':
                return 'True'
            elif create_method:
                return Response(create_method, status=status.HTTP_400_BAD_REQUEST)
        elif delete:
            delete_method = applicationfun.delete_application(request)
            if delete_method:
                return Response({'message': 'The application has been successfully removed'},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'You do not have access to this action'}, status=status.HTTP_403_FORBIDDEN)
        elif accept:
            accept_method = applicationfun.accept_application(request)
            if accept_method == 404:
                return Response({'message': 'Application Not Found.'}, status=status.HTTP_404_NOT_FOUND)
            elif accept_method:
                return Response({'message': 'The Application has been successfully accepted'},
                                status=status.HTTP_200_OK)
            elif not accept_method:
                return Response({'message': 'You do not have access to this action'}, status=status.HTTP_403_FORBIDDEN)


class TaskList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: TaskSerializer(many=True)},
    )
    def get(self, request):
        """
        Получает список задач пользователя.
        """
        tasks = Task.objects.filter(user=UserProfile.objects.get(id=get_user_id_from_token(request)))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            serializer.save(user=UserProfile.objects.get(id=user_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskEnvironmentAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            return Response({'message': 'User has no provided.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(data=request.data)
        try:
            environment = Environment.objects.get(id=pk, user=UserProfile.objects.get(id=user_pk))
        except Environment.DoesNotExist:
            try:
                environment = Environment.objects.get(id=pk)
            except Environment.DoesNotExist:
                return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
            try:
                admin = Admin.objects.get(environment=environment,
                                          user=UserProfile.objects.get(id=get_user_id_from_token(request)),
                                          is_admin=True)
            except Admin.DoesNotExist:
                return Response({'message': 'You Do Not Have access'}, status=status.HTTP_404_NOT_FOUND)
            except UserProfile.DoesNotExist:
                return Response({'message': 'You have to chose one of the admins'}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({'message': 'You have to chose one of the admins'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(user=UserProfile.objects.get(id=task_user_pk), environment=environment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, request):
        return get_object_or_404(Task, id=pk, user=UserProfile.objects.get(id=get_user_id_from_token(request)))

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task.is_deleted = True
        return Response({'message': 'Task has been successfully removed'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnvironmentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            return Response({'message': 'You have not saved environments.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EnvironmentSerializer(environments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        request_body=EnvironmentSerializer,
        responses={
            201: 'Environment has been successfully created',
            400: 'Environment with this name is already taken. Please try again.'
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
            if Environment.objects.filter(name=serializer.validated_data['name'], user=user):
                return Response({'message': 'Environment with this name is already taken. Please try again.'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=user)
            saving_environment = SavedEnvironment.objects.create(user=user,
                                                                 environment=Environment.objects.get(
                                                                     id=serializer.data.get('id')))
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
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: EnvironmentSerializer()},
        query_serializer=EnvironmentQuerySerializer()
    )
    def get(self, request, pk):
        """
        Получает информацию об определенном окружении.
        """

        query_serializer = EnvironmentQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        password = query_serializer.validated_data.get('password')
        try:
            environment = Environment.objects.filter(id=pk, is_deleted=False)
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        if not environment:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        user_id = get_user_id_from_token(request)  # Получаем первичный ключ пользователя
        user = UserProfile.objects.get(id=get_user_id_from_token(request))
        # Проверяем, существует ли уже запись для данного пользователя и окружения
        saved_environment_qs = SavedEnvironment.objects.filter(user=user_id, environment=pk)

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
                environment = Environment.objects.filter(id=pk, password=password)
                if environment.exists():
                    data = {
                        'user': user_id,
                        'environment': pk,
                    }
                else:
                    return Response({'message': 'Incorrect password'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'message': 'Environment Not Found'}, status=status.HTTP_404_NOT_FOUND)
            saving_environment = SavedEnvironmentSerializer(data=data)
            if saving_environment.is_valid():
                saved_environment = saving_environment.save()
            else:
                return Response(saving_environment.errors, status=status.HTTP_400_BAD_REQUEST)
        application = ApplicationActions(environment, user, pk)
        create_application = application.get(request, pk, True)
        if create_application == 'True':
            pass
        else:
            return Response(create_application, status=status.HTTP_400_BAD_REQUEST)
        saved_environment.save()  # Сохраняем изменения или новую запись
        environment_instance = environment.first()
        serializer = EnvironmentSerializer(environment_instance, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                           description="пароль от окружения для его удаления"),
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
                if Environment.objects.filter(id=pk, user=UserProfile.objects.get(
                        id=get_user_id_from_token(request))):
                    if Environment.objects.filter(id=pk, password=password):
                        is_access = True
                    else:
                        return Response({'message': 'Incorrect password.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    pass
            else:
                return Response({'message': 'Password has no provided.'}, status=status.HTTP_400_BAD_REQUEST)
            environment = self.get_object(pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        if is_access:
            environment.is_deleted = True
            environment.save()
        else:
            return Response({'message': 'You do not have permission to delete this environment'},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({'message': 'Environment has been removed successfully.'}, status=status.HTTP_200_OK)


class EnvironmentAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Environment,
                                 id=pk)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(id=get_user_id_from_token(request))
            environment = Environment.objects.get(id=pk)
            admins = Admin.objects.filter(
                environment=environment)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        if Admin.objects.filter(environment=environment, user=user).exists() or Environment.objects.filter(
                user=user).exists():
            pass
        else:
            return Response({'message': 'You do not have any access to this environment'},
                            status=status.HTTP_403_FORBIDDEN)
        if admins:
            serializer = AdminEnvironmentSerializer(admins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'This environment do not have any admins'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'admin_pk': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID администратора окружения"),
            },
            required=['admin_pk']
        ),
        responses={201: 'You have successfully added your friend to environment'},
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
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        admin_pk = request.data.get('admin_pk')
        if admin_pk is None:
            return Response({'message': 'admin_pk has no provided'}, status=status.HTTP_400_BAD_REQUEST)
        environment_check = Environment.objects.filter(user=user)
        if environment_check:
            is_access = True
        elif Admin.objects.filter(user=user):
            is_access = True
        elif not is_access:
            return Response({'message': 'You do not have permission to add your friend!!!'},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user_admin_pk = UserProfile.objects.get(id=admin_pk)
            admin = Admin.objects.filter(user=user_admin_pk, environment=environment).first()
            if admin is None:
                if is_access:
                    admin = Admin.objects.create(environment=environment, user=UserProfile.objects.get(id=admin_pk))
                    if request.data.get('is_superadmin'):
                        admin.save(is_superadmin=True, is_admin=True)
                    return Response({'message': 'You have successfully added your friend to environment'},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'You do not have permission to add your friend!'},
                                    status=status.HTTP_403_FORBIDDEN)
            return Response({'message': 'This admin is already associated with this environment'},
                            status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
                Admin.objects.get(id=get_user_id_from_token(request), is_superadmin=True, environment=environment)
                is_access_to_delete_superadmin = False
            except Admin.DoesNotExist:
                return Response({'message': 'You Do Not Have access.'}, status=status.HTTP_403_FORBIDDEN)
            except Http404:
                return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        if is_access_to_delete_superadmin:
            try:
                admin = Admin.objects.get(id=admin_pk, environment=environment)
            except Admin.DoesNotExist:
                return Response({'message': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                admin = Admin.objects.get(id=admin_pk, is_superadmin=True, environment=environment)
            except Admin.DoesNotExist:
                try:
                    admin = Admin.objects.get(id=admin_pk, environment=environment)
                except Admin.DoesNotExist:
                    return Response({'message': 'You do not have access'}, status=status.HTTP_403_FORBIDDEN)
        admin.delete()
        return Response({'message': 'Admin deleted successfully'}, status=status.HTTP_200_OK)


class AdminActionsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
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
            admin = Admin.objects.filter(user=UserProfile.objects.get(id=get_user_id_from_token(request)))
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        if not admin.exists():
            if Environment.objects.filter(id=environment_pk,
                                          user=UserProfile.objects.get(id=get_user_id_from_token(request))):
                is_admin = True
            else:
                return Response({'message': 'You Do Not Have access'}, status=status.HTTP_404_NOT_FOUND)
        if is_admin:
            task = Task.objects.filter(environment=environment,
                                       is_deleted=False,
                                       completed=False)
        else:
            task = Task.objects.filter(environment=environment,
                                       user=UserProfile.objects.get(id=get_user_id_from_token(request)),
                                       is_deleted=False,
                                       completed=False)

        if not task:
            return Response({'message': 'You have not any tasks.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class EnvironmentTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_pk': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID задачи"),
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
                                                  user=UserProfile.objects.get(id=user_pk))
        except Environment.DoesNotExist:
            try:
                environment = Environment.objects.get(id=environment_pk)
            except Environment.DoesNotExist:
                return Response(
                    {'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND
                )
            try:
                admin = Admin.objects.get(environment=environment,
                                          user=UserProfile.objects.get(id=get_user_id_from_token(request)),
                                          is_admin=True)
            except Admin.DoesNotExist:
                return Response(
                    {'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND
                )
        task_pk = request.data.get('task_pk')
        try:
            task = Task.objects.get(environment=environment,
                                    id=task_pk)
        except Task.DoesNotExist:
            return Response(
                {'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND
            )
        task.completed = True
        return Response({'message': 'Task has been completed'}, status=status.HTTP_200_OK)


def build_comment_tree(comment, comments_dict):
    comment_data = CommentsSerializer(instance=comment).data
    children_comments = comments_dict.get(comment.id, [])

    if children_comments:
        comment_data['children'] = [build_comment_tree(child, comments_dict) for child in children_comments]

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

            main_comments = [comment for comment in comments if not comment.parent_id]

            return main_comments, comments_dict
        except Task.DoesNotExist:
            logger.warning(f"Failed to get comments. Task not found.")
            raise Response({"message": "Task not found"}, status=404)
        except Exception as e:
            logger.error(f"An error occurred while processing the request: {str(e)}")
            raise Response({"error": str(e)}, status=500)

    def get(self, request, task_id):
        try:
            main_comments, comments_dict = self.get_object(task_id)
            main_comments_tree = [build_comment_tree(comment, comments_dict) for comment in main_comments]
            return Response(main_comments_tree, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred while processing the request: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'parent_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                'comment_text': openapi.Schema(type=openapi.TYPE_STRING),
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
                    new_comment = serializer.save(user=user_profile,
                                                  task=task)  # Сначала сохраняем новый комментарий
                    parent_comment.children.add(
                        new_comment)  # Устанавливаем связь между родительским и дочерним комментариями
                else:
                    serializer.save(user=user_profile, task=task)

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            logger.warning(f"Failed to create a new comment. User profile not found.")
            return Response({"message": "You have not registered yet"}, status=status.HTTP_404_NOT_FOUND)
        except Task.DoesNotExist:
            logger.warning(f"Failed to get comments. Task not found.")
            return Response({"message": "Task not found"}, status=404)
        except Exception as e:
            logger.error(f"An error occurred while processing the request: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, _comment_id):
        try:
            return Comment.objects.get(id=_comment_id)
        except Comment.DoesNotExist:
            logger.warning(f"Failed to get comments. Comment not found.")
            raise Http404({"message": "Comment not found"})
        except Exception as e:
            logger.error(f"An error occurred while processing the request: {str(e)}")
            raise Response({"error": str(e)}, status=500)

    @transaction.atomic
    def delete_comment_chain(self, comment):
        # Recursively delete comment chain
        child_comments = Comment.objects.filter(parent_id=comment.id)
        for child_comment in child_comments:
            self.delete_comment_chain(child_comment)
            child_comment.delete()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        security=[],
    )
    def delete(self, request, comment_id):
        try:
            user_id = get_user_id_from_token(request)
            user_profile = UserProfile.objects.get(id=user_id)
            comment = Comment.objects.get(id=comment_id, user=user_profile)
            logger.info(f"Attempting to delete comment with ID {comment_id}.")
        except Comment.DoesNotExist:
            logger.warning(f"Failed to delete Comment. Comment with ID {comment_id} not found.")
            return Response({"message": "Comment Not Found"}, status=404)
        except Exception as e:
            logger.error(f"An error occurred while processing the request: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Delete the entire comment chain
        self.delete_comment_chain(comment)

        # Delete the parent comment
        comment.delete()

        return Response({'message': 'comment has been successfully deleted!'}, status=204)
