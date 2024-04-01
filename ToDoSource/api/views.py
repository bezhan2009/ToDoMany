from django.shortcuts import get_object_or_404
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from django.db import transaction
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
                return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            serializer.save(user=UserProfile.objects.get(id=task_user_pk), environment=environment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Task, id=pk)

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
            task = self.get_object(pk)
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
            task = self.get_object(pk)
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
            task = self.get_object(pk)
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
        Получает список всех окружений.
        """
        try:
            environments = Environment.objects.all()
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EnvironmentSerializer(environments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        request_body=EnvironmentSerializer,
        responses={201: 'Environment has been successfully created'},
    )
    def post(self, request):
        """
        Создает новое окружение.
        """
        user_pk = get_user_id_from_token(request)
        serializer = EnvironmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=UserProfile.objects.get(id=user_pk))
            return Response(
                {'message': 'Environment has been successfully created'}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnvironmentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Environment, pk=pk)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: EnvironmentSerializer()},
    )
    def get(self, request, pk):
        """
        Получает информацию об определенном окружении.
        """
        try:
            environment = self.get_object(pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EnvironmentSerializer(environment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        responses={200: 'Environment has been removed successfully'},
    )
    def delete(self, request, pk):
        """
        Удаляет окружение.
        """
        try:
            environment = self.get_object(pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        environment.is_deleted = True
        return Response({'message': 'Environment has been removed successfully'}, status=status.HTTP_200_OK)


class EnvironmentAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user_pk):
        return get_object_or_404(Environment,
                                 id=pk,
                                 user=UserProfile.objects.get(id=user_pk))

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
        try:
            environment = self.get_object(pk, user_pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        admin_pk = request.data.get('admin_pk')
        Admin.objects.create(environment=environment, user=UserProfile.objects.get(id=admin_pk))
        return Response({'message': 'You have successfully added your friend to environment'},
                        status=status.HTTP_201_CREATED)


class EnvironmentAdminAction(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user_pk):
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
            environment = self.get_object(pk, user_pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        Admin.objects.get(id=admin_pk).delete()
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
        try:
            environment = Environment.objects.get(id=environment_pk)
            admin = Admin.objects.get(user=UserProfile.objects.get(id=get_user_id_from_token(request)))
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Admin.DoesNotExist:
            return Response({'message': 'You Do Not Have access'}, status=status.HTTP_404_NOT_FOUND)
        task = Task.objects.filter(environment=environment,
                                   user=UserProfile.objects.get(id=get_user_id_from_token(request)),
                                   is_deleted=False,
                                   completed=False)
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
