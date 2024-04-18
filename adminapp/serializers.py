from rest_framework import serializers

from adminapp.models import Admin


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