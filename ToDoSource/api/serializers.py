"""
This file contains the serializers for the models.
"""

from rest_framework import serializers

from ToDoSource.models import (
    UserProfile,
    Task,
    Environment,
    Comment,
    SavedEnvironment,
    Admin,
    Application,
    TeamPerson,
    Team
)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the user profile model.
    """
    age = serializers.IntegerField(required=False)
    is_activate = serializers.BooleanField(required=False, default=True)

    def create(self, validated_data):
        """
        This function creates a new user.
        """
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        This function updates the user profile.
        """
        instance.age = validated_data.get(
            'age', instance.age
        )
        instance.is_activate = validated_data.get(
            'is_activate',
            instance.is_activate
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the user profile model.
        """
        model = UserProfile
        fields = ['id', 'username', 'password', 'age']


class TaskSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the task model.
    """
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        required=False
    )

    def create(self, validated_data):
        """
        This function creates a new task.
        """
        task = Task.objects.create(**validated_data)
        return task

    def update(self, instance, validated_data):
        """
        This function updates the task.
        """
        instance.task_name = validated_data.get(
            'task_name', instance.task_name
        )
        instance.task_description = validated_data.get(
            'task_description',
            instance.task_description
        )
        instance.task_status = validated_data.get(
            'task_status',
            instance.task_status
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the task model.
        """
        model = Task
        fields = '__all__'

    def get_fields(self):
        """
        This function is used to get the fields of the task model.
        """
        fields = super().get_fields()
        fields.pop('user', None)
        fields.pop('environment', None)
        return fields


class EnvironmentSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the environment model.
    """

    def create(self, validated_data):
        """
        This function creates a new environment.
        """
        environment = Environment.objects.create(**validated_data)
        return environment

    def update(self, instance, validated_data):
        """
        This function updates the environment.
        """
        instance.environment_name = validated_data.get(
            'environment_name', instance.environment_name
        )
        instance.environment_description = validated_data.get(
            'environment_description',
            instance.environment_description
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the environment model.
        """
        model = Environment
        fields = '__all__'

    def get_fields(self):
        """
        This function is used to get the fields of the environment model.
        """
        fields = super().get_fields()
        fields.pop('user', None)
        return fields


class CommentChildrenSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the child comments.
    """
    id = serializers.IntegerField()
    comment_text = serializers.CharField()
    parent_id = serializers.IntegerField()

    def create(self, validated_data):
        """
        This function creates a new comment.
        """
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        """
        This function updates the comment.
        """
        instance.comment_text = validated_data.get(
            'comment_text', instance.comment_text
        )
        instance.parent_id = validated_data.get(
            'parent_id',
            instance.parent_id
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the child comments.
        """
        model = Comment
        fields = ['id', 'comment_text', 'parent_id']


class CommentsSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the comments.
    """
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        required=False
    )
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False
    )

    def create(self, validated_data):
        """
        This function creates a new comment.
        """
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.comment_text = validated_data.get(
            'comment_text', instance.comment_text
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the comments.
        """
        model = Comment
        fields = '__all__'


class CommentMainSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the main comments.
    """
    id = serializers.IntegerField()
    comment_text = serializers.CharField()
    parent_id = serializers.IntegerField()
    children = CommentChildrenSerializer(many=True, read_only=True)

    def create(self, validated_data):
        """
        This function creates a new comment.
        """
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        """
        This function updates the comment.
        """
        instance.comment_text = validated_data.get(
            'comment_text', instance.comment_text
        )
        instance.parent_id = validated_data.get(
            'parent_id',
            instance.parent_id
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the main comments.
        """
        model = Comment
        fields = ['id', 'comment_text', 'parent_id', 'children']


class SavedEnvironmentSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the saved environments.
    """

    def create(self, validated_data):
        """
        This function creates a new saved environment.
        """
        saved_environment = SavedEnvironment.objects.create(**validated_data)
        return saved_environment

    def update(self, instance, validated_data):
        """
        This function updates the saved environment.
        """
        instance.environment_name = validated_data.get(
            'environment_name', instance.environment_name
        )
        instance.environment_description = validated_data.get(
            'environment_description',
            instance.environment_description
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the saved environments.
        """
        model = SavedEnvironment
        fields = '__all__'


class AdminEnvironmentSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the admin environments.
    """

    def create(self, validated_data):
        """
        This function creates a new admin environment.
        """
        admin = Admin.objects.create(**validated_data)
        return admin

    def update(self, instance, validated_data):
        """
        This function updates the admin environment.
        """
        instance.is_admin = validated_data.get(
            'is_admin', instance.is_admin
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the admin environments.
        """
        model = Admin
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the applications.
    """

    def create(self, validated_data):
        """
        This function creates a new application.
        """
        application = Application.objects.create(**validated_data)
        return application

    def update(self, instance, validated_data):
        """
        This function updates the application.
        """
        instance.is_accept = validated_data.get(
            'is_accept', instance.is_accept
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the applications.
        """
        model = Application
        fields = '__all__'


class EnvironmentQuerySerializer(serializers.Serializer):
    """
    This class is used to serialize the environment query.
    """
    password = serializers.CharField(
        required=False,
        help_text="Write the of environment"
    )

    def create(self, validated_data):
        """
        This function creates a new environment.
        """
        environment = Environment.objects.create(**validated_data)
        return environment

    def update(self, instance, validated_data):
        """
        This function updates the environment.
        """
        instance.password = validated_data.get(
            'password', instance.password
        )
        instance.save()
        return instance


class ApplicationQuerySerializer(serializers.Serializer):
    """
    This class is used to serialize the application query.
    """
    get = serializers.BooleanField(required=False, default=False)
    create = serializers.BooleanField(required=False, default=False)
    delete = serializers.BooleanField(required=False, default=False)
    accept = serializers.BooleanField(required=False, default=False)
    application_pk = serializers.IntegerField(required=False)
    environment_pk = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """
        This function creates a new application.
        """
        application = Application.objects.create(**validated_data)
        return application

    def update(self, instance, validated_data):
        """
        This function updates the application.
        """
        instance.is_accept = validated_data.get(
            'is_accept', instance.is_accept
        )
        instance.save()
        return instance


class AdminSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the admin model.
    """

    def create(self, validated_data):
        """
        This function creates a new admin.
        """
        admin = Admin.objects.create(**validated_data)
        return admin

    def update(self, instance, validated_data):
        """
        This function updates the admin.
        """
        instance.is_admin = validated_data.get(
            'is_admin', instance.is_admin
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the admin model.
        """
        model = Admin
        fields = '__all__'


class TeamPersonSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the team person model.
    """

    def create(self, validated_data):
        """
        This function creates a new team person.
        """
        team_person = TeamPerson.objects.create(**validated_data)
        return team_person

    def update(self, instance, validated_data):
        """
        This function updates the team person.
        """
        instance.is_admin = validated_data.get(
            'is_admin', instance.is_admin
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the team person model.
        """
        model = TeamPerson
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    """
    This class is used to serialize the team model.
    """
    team_people = TeamPersonSerializer(many=True, read_only=True)

    def create(self, validated_data):
        """
        This function creates a new team.
        """
        team = Team.objects.create(**validated_data)
        return team

    def update(self, instance, validated_data):
        """
        This function updates the team.
        """
        instance.user = validated_data.get(
            'user', instance.user
        )
        instance.date = validated_data.get(
            'date', instance.date
        )
        instance.save()
        return instance

    class Meta:
        """
        This class is used to define the fields of the team model.
        """
        model = Team
        fields = ['id', 'user', 'date', 'team_people']


class TeamQuerySerializer(serializers.Serializer):
    """
    This class is used to serialize the team query.
    """
    selected_team = serializers.ListField(required=True)

    def create(self, validated_data):
        """
        This function creates a new team.
        """

        team = Team.objects.create(**validated_data)
        return team

    def update(self, instance, validated_data):
        """
        This function updates the team.
        """
        instance.selected_team = validated_data.get(
            'selected_team', instance.selected_team
        )
        instance.save()
        return instance
