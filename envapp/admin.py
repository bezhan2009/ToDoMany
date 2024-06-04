from django.contrib import admin
from .models import Environment, SavedEnvironment

admin.site.register(Environment)
admin.site.register(SavedEnvironment)
