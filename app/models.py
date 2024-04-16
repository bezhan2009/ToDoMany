from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from envapp.models import Environment


# Create your models here.
class Application(models.Model):
    user = models.ForeignKey(User, related_name='applications_as_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='applications_as_to_user', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    is_accept = models.BooleanField(default=False)

    def __str__(self):
        return f"Environment: {self.environment}\n User: {self.user}"
