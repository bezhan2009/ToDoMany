from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from adminapp.models import Admin
from envapp.models import Environment
from taskapp.models import Task
from taskapp.serializers import TaskSerializer
from userapp.models import UserProfile
from utils.tokens import get_user_id_from_token


# Create your views here.
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
