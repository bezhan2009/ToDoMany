from rest_framework import serializers

from userapp.models import UserProfile
from .models import Task


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
