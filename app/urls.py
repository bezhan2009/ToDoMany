from django.urls import path

from .views import ApplicationList, ApplicationDetails

urlpatterns = [
    path('<int:environment_pk>/',
         ApplicationList.as_view(),
         name='application'
         ),
    path('detail/<int:application_pk>/',
         ApplicationDetails.as_view(),
         name='application'
         )
]
