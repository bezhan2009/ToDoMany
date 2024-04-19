from rest_framework import serializers

from teamapp.models import TeamPerson, Team


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
