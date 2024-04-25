from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from taskapp.models import Task


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')
    comment_text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
