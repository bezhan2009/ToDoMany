from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ToDoSource.models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'password', 'age']
