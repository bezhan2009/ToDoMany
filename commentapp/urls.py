from django.urls import path

from .views import (
    CommentList,
    CommentDetail
)

urlpatterns = [
    path('<int:task_id>/',
         CommentList.as_view(),
         name='comment-list'
         ),
    path('<int:comment_id>/detail/',
         CommentDetail.as_view(),
         name='comment-detail'
         )
]
