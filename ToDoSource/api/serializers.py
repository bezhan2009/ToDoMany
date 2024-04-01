from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ToDoSource.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'age']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        fields.pop('user', None)
        fields.pop('environment', None)
        return fields


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        fields.pop('user', None)
        return fields
