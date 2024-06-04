from rest_framework import serializers

from .models import Application


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
    """
    def create(self, validated_data):
        '''
        This function creates a new application.
        '''
        application = Application.objects.create(**validated_data)
        return application
    """
    def update(self, instance, validated_data):
        """
        This function updates the application.
        """
        instance.is_accept = validated_data.get(
            'is_accept', instance.is_accept
        )
        instance.save()
        return instance
