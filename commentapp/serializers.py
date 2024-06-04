from rest_framework import serializers

from taskapp.models import Task
from userapp.models import UserProfile
from .models import Comment


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
