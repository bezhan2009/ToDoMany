from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from adminapp.models import Admin
from app.views import ApplicationActions
from envapp.models import Environment, SavedEnvironment
from envapp.serializers import EnvironmentSerializer, EnvironmentQuerySerializer, SavedEnvironmentSerializer, \
    AdminEnvironmentSerializer
from userapp.models import UserProfile
from utils.tokens import get_user_id_from_token


# Create your views here.
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