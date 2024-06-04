from django.urls import path

from .views import (
    TeamList,
    TeamPersonList
)

urlpatterns = [
    path('',
         TeamList.as_view(),
         name='team-list'
         ),
    path('person/<int:team_pk>/',
         TeamPersonList.as_view(),
         name='team-person-list'
         )
]
