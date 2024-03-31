from django.contrib import admin
from .models import UserProfile, Task, Environment, Admin
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Environment)
admin.site.register(Admin)
