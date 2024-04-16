from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#
class UserProfile(User):
    age = models.IntegerField()
    is_activate = models.BooleanField(default=True)


class Environment(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    money = models.IntegerField(null=False, default=0)
    deadline = models.DateTimeField(null=True, blank=True, default=1)  # Добавляем поле для срока выполнения задачи

    def __str__(self):
        return self.description


class Admin(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')
    comment_text = models.TextField()
    date = models.DateTimeField(default=timezone.now)


class SavedEnvironment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.environment.name


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    is_accept = models.BooleanField(default=False)

    def __str__(self):
        return f"Environment: {self.environment}\n User: {self.user}"


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class TeamPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}\'s team: {self.team}"

