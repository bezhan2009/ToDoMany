from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from userapp.models import UserProfile


# Create your models here.
class Environment(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SavedEnvironment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.environment.name
