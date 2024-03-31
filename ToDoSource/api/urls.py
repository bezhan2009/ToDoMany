
from django.contrib import admin
from django.urls import path, include
from ToDoSource.api.views import *

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('environment/', EnvironmentList.as_view(), name='environment-list'),
    path('environment/<int:pk>/', EnvironmentDetail.as_view()),
    path('environment/action/<int:pk>/', EnvironmentAction.as_view(), name='environment-action'),
    path('environment/admin/action/<int:pk>/', AdminActionsView.as_view(), name='admin-action')
]
