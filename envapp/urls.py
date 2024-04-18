from django.urls import path

from adminapp.views import AdminActionsView
from taskapp.views import EnvironmentTaskView
from .views import (
    EnvironmentList,
    EnvironmentDetail,
    EnvironmentAction
)

urlpatterns = [
    path('',
         EnvironmentList.as_view(),
         name='environment-list'
         ),
    path('<int:pk>/',
         EnvironmentDetail.as_view(),
         name='environment-detail'
         ),
    path('action/<int:pk>/',
         EnvironmentAction.as_view(),
         name='environment-action'
         ),
    path('admin/action/<int:environment_pk>/',
         AdminActionsView.as_view(),
         name='admin-action'
         ),
    path('task/<int:pk>/',
         EnvironmentTaskView.as_view(),
         name='environment-task'
         )
]
