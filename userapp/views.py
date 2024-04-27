import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from userapp.serializers import UserProfileSerializer

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


# Fix files
