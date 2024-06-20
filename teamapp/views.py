from django.http import Http404
from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from adminapp.models import Admin
from app.models import Application
from teamapp.models import Team, TeamPerson
from teamapp.serializers import TeamSerializer, TeamQuerySerializer
from userapp.models import UserProfile
from utils.tokens import get_user_id_from_token


# Create your views here.
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
