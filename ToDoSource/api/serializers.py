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


class CommentChildrenSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    comment_text = serializers.CharField()
    parent_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'parent_id']


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), required=False)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentMainSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    comment_text = serializers.CharField()
    parent_id = serializers.IntegerField()
    children = CommentChildrenSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'parent_id', 'children']


class SavedEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedEnvironment
        fields = '__all__'


class AdminEnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class EnvironmentQuerySerializer(serializers.Serializer):
    password = serializers.CharField(required=False, help_text="Write the of environment")


class ApplicationQuerySerializer(serializers.Serializer):
    get = serializers.BooleanField(required=False, default=False)
    create = serializers.BooleanField(required=False, default=False)
    delete = serializers.BooleanField(required=False, default=False)
    accept = serializers.BooleanField(required=False, default=False)
    application_pk = serializers.IntegerField(required=False)
    environment_pk = serializers.IntegerField(required=False)


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

