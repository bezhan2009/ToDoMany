from django.urls import path

from taskapp.views import TaskDetail
from taskapp.views import (
    TaskList,
    TaskEnvironmentAction
)

urlpatterns = [
    path('',
         TaskList.as_view(),
         name='task-list'
         ),
    path('<int:pk>/',
         TaskDetail.as_view(),
         name='task-detail'
         ),
    path('for_environment/<int:pk>/',
         TaskEnvironmentAction.as_view(),
         name='task-environment-action')
]
