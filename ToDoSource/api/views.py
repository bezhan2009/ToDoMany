
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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

    def get(self, request):
        tasks = Task.objects.all()
        if len(tasks) > 0:
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No tasks found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_pk = get_user_id_from_token(request)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=UserProfile.objects.get(id=user_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Task, id=pk)

    def get(self, request, pk):
        try:
            task = self.get_object(pk)
        except Http404:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            task = self.get_object(pk)
        except Http404:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task.is_deleted = True
        return Response({'message': 'Task has been successfully removed'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        try:
            task = self.get_object(pk)
        except Http404:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnvironmentList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            environments = Environment.objects.all()
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EnvironmentSerializer(environments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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

    def get(self, request, pk):
        try:
            environment = self.get_object(pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EnvironmentSerializer(environment, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
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
        return get_object_or_404(Environment, id=pk, user=UserProfile.objects.get(id=user_pk))

    def post(self, request, pk):
        user_pk = get_user_id_from_token(request)
        try:
            environment = self.get_object(pk, user_pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        admin_pk = request.data.get('admin_pk')
        Admin.objects.create(environment=environment, user=UserProfile.objects.get(id=admin_pk))
        return Response({'message': 'You have successfully added your friend to environment'}, status=status.HTTP_201_CREATED)


class EnvironmentAdminAction(APIView):
    def get_object(self, pk, user_pk):
        return get_object_or_404(Environment, pk=pk, user=UserProfile.objects.get(id=user_pk))

    def delete(self, request, pk, admin_pk):
        user_pk = get_user_id_from_token(request)
        try:
            environment = self.get_object(pk, user_pk)
        except Http404:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)

        Admin.objects.get(id=admin_pk).delete()
        return Response({'message': 'Admin deleted successfully'}, status=status.HTTP_200_OK)


class AdminActionsView(APIView):
    def get(self, request, environment_pk):
        try:
            environment = Environment.objects.get(id=environment_pk)
            admin = Admin.objects.get(user=UserProfile.objects.get(id=get_user_id_from_token(request)))
        except Environment.DoesNotExist:
            return Response({'message': 'Environment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Admin.DoesNotExist:
            return Response({'message': 'You Do Not Have access'}, status=status.HTTP_404_NOT_FOUND)
        task = Task.objects.filter(environment=environment, user=UserProfile.objects.get(id=get_user_id_from_token(request)), is_deleted=False, completed=False)
        serializer = TaskSerializer(task, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
