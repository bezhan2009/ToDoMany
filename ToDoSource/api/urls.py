
from django.urls import path
from ToDoSource.api.views import *

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/for_environment/<int:pk>/', TaskEnvironmentAction.as_view(), name='task-environment-action'),

    path('environment/', EnvironmentList.as_view(), name='environment-list'),
    path('environment/<int:pk>/', EnvironmentDetail.as_view()),

    path('environment/action/<int:pk>/', EnvironmentAction.as_view(), name='environment-action'),
    path('environment/admin/action/<int:environment_pk>/', AdminActionsView.as_view(), name='admin-action'),

    path('environment/task/<int:pk>/', EnvironmentTaskView.as_view(), name='environment-task'),

    path('comment/<int:task_id>/', CommentList.as_view(), name='comment'),
    path('comment/<int:comment_id>/detail/', CommentDetail.as_view(), name='comment_detail'),

    path('application/<int:pk>/', ApplicationActions.as_view(), name='application'),
]

# Just Checking
