from django.urls import path

from .views import ApplicationActions

urlpatterns = [
    path('',
         ApplicationActions.as_view(),
         name='application'
         )
]
