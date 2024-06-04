from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(User):
    age = models.IntegerField()
    is_activate = models.BooleanField(default=True)
