from django.db import models
from django.contrib.auth.models import User
from django.urls import path, include

from ToDoSource import views

urlpatterns = [
    path('ping', views.ping, name='ping'),
    path('api/', include('ToDoSource.api.urls'))
]
