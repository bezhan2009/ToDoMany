from rest_framework import serializers

from adminapp.models import Admin
from .models import Environment, SavedEnvironment


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
