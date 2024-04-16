from django.urls import path

from .views import AdminPermissions

urlpatterns = [
    path('<int:environment_pk>/<int:admin_pk>/',
         AdminPermissions.as_view(),
         name='admin-actions'
         )
]
