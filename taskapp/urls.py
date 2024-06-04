from django.urls import path
from taskapp.views import (
    TaskDetail,
    TaskList,
    TaskEnvironmentAction
)
from taskapp.views import EnvironmentTaskView
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
         name='task-environment-action'),

    path('task/<int:environment_pk>/',
         EnvironmentTaskView.as_view(),
         name='environment-task'
         )
]
