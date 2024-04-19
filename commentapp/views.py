from django.db import transaction
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from commentapp.models import Comment
from commentapp.serializers import CommentsSerializer
from commentapp.utils import build_comment_tree
from taskapp.models import Task
import logging

from userapp.models import UserProfile
from utils.tokens import get_user_id_from_token

logger = logging.getLogger(__name__)

# Create your views here.
class CommentList(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get_object(self, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            comments = Comment.objects.filter(task=task)
            comments_dict = {comment.id: [] for comment in comments}

            for comment in comments:
                if comment.parent_id:
                    comments_dict[comment.parent_id].append(comment)

            main_comments = [comment for comment in comments
                             if not comment.parent_id]

            return main_comments, comments_dict
        except Task.DoesNotExist:
            logger.warning("Failed to get comments. Task not found.")
            raise Response(
                data={"message": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            raise Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request, task_id):
        try:
            main_comments, comments_dict = self.get_object(task_id)
            main_comments_tree = [build_comment_tree(
                comment,
                comments_dict
            ) for comment in main_comments]
            return Response(
                data=main_comments_tree,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'parent_id': openapi.Schema(
                    type=openapi.TYPE_NUMBER
                ),
                'comment_text': openapi.Schema(
                    type=openapi.TYPE_STRING
                ),
            },
            required=['comment_text']
        ),
        security=[],
    )
    def post(self, request, task_id):
        try:
            user_id = get_user_id_from_token(request)
            user_profile = UserProfile.objects.get(id=user_id)
            serializer = CommentsSerializer(data=request.data)
            if serializer.is_valid():
                parent_comment_id = request.data.get('parent_id')
                task = Task.objects.get(id=task_id)

                if parent_comment_id:
                    parent_comment = Comment.objects.get(id=parent_comment_id)
                    new_comment = serializer.save(
                        user=user_profile,
                        task=task)  # Сначала сохраняем новый комментарий

                    parent_comment.children.add(
                        new_comment
                    )
                else:
                    serializer.save(
                        user=user_profile,
                        task=task
                    )

                return Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except UserProfile.DoesNotExist:
            logger.warning(
                "Failed to create a new comment. User profile not found."
            )
            return Response(
                data={"message": "You have not registered yet"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Task.DoesNotExist:
            logger.warning(
                "Failed to get comments. Task not found."
            )
            return Response(
                data={"message": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommentDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, _comment_id):
        try:
            return Comment.objects.get(id=_comment_id)
        except Comment.DoesNotExist:
            logger.warning(
                "Failed to get comments. Comment not found."
            )
            raise Http404({"message": "Comment not found"})
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            raise Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def delete_comment_chain(self, comment):
        # Recursively delete comment chain
        child_comments = Comment.objects.filter(parent_id=comment.id)
        for child_comment in child_comments:
            self.delete_comment_chain(child_comment)
            child_comment.delete()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING),
        ],
        security=[],
    )
    def delete(self, request, comment_id):
        try:
            user_id = get_user_id_from_token(request)
            user_profile = UserProfile.objects.get(
                id=user_id
            )
            comment = Comment.objects.get(
                id=comment_id,
                user=user_profile
            )
            logger.info(
                "Attempting to delete comment with ID %s.",
                str(comment_id)
            )
        except Comment.DoesNotExist:
            logger.warning(
                "Failed to delete Comment. Comment with ID %s not found.",
                str(comment_id)
            )
            return Response(
                data={"message": "Comment Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                "An error occurred while processing the request: %s",
                str(e)
            )
            return Response(
                data={"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Delete the entire comment chain
        self.delete_comment_chain(comment)

        # Delete the parent comment
        comment.delete()

        return Response(
            data={'message': 'comment has been successfully deleted!'},
            status=status.HTTP_200_OK
        )