from django.urls import path
from .views import AdminPermissions, AdminActionsView

app_name = 'adminapp'

urlpatterns = [
    path('<int:environment_pk>/', AdminActionsView.as_view(), name='admin-actions'),
    path('<int:environment_pk>/<int:admin_pk>/', AdminPermissions.as_view(), name='admin-permissions'),
]
