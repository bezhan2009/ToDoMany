from rest_framework import serializers

from .models import UserProfile


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
