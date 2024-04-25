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
