from django.db import models
from django.utils import timezone

from envapp.models import Environment
from userapp.models import UserProfile


# Create your models here.
class Admin(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
