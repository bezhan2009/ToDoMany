import logging
from utils.tokens import get_user_id_from_token
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken


logger = logging.getLogger('userapp.views')


class UserView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    def post(self, request):
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


class UserProfileDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, _id):
        return get_object_or_404(UserProfile, id=_id)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        security=[],
    )
    def get(self, request):
        user_id = get_user_id_from_token(request)
        try:
            user = self.get_user(user_id)
            logger.info(f"User with ID {user_id} retrieved successfully.")
        except UserProfile.DoesNotExist:
            logger.warning(f"Failed to retrieve user. User with ID {user_id} not found.")
            return Response({"message": "User Not Found"}, status=404)

        serializer = UserProfileSerializer(user, many=False)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username']
        ),
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>",
                              type=openapi.TYPE_STRING),
        ],
        security=[],
    )
    def put(self, request):
        user_id = get_user_id_from_token(request)
        try:
            user = self.get_user(user_id)
            logger.info(f"Attempting to update user with ID {user_id}.")
        except UserProfile.DoesNotExist:
            logger.warning(f"Failed to update user. User with ID {user_id} not found.")
            return Response({"message": "User Not Found."}, status=404)

        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if 'password' in request.data or 'is_deleted' in request.data or 'is_superuser' in request.data:
            return Response({"message": "Changing password, is_superuser is not allowed."}, status=403)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User with ID {user_id} updated successfully.")
            return Response(serializer.data, status=200)
        logger.error(f"Failed to update user with ID {user_id}: {serializer.errors}")
        return Response(serializer.errors, status=401)
