from django.db import models
from django.utils import timezone

from envapp.models import Environment
from userapp.models import UserProfile


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, null=True)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    money = models.IntegerField(null=False, default=0)
    deadline = models.DateTimeField(null=True, blank=True, default=timezone.now)  # Исправлено

    def __str__(self):
        return self.description
