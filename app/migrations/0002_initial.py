# Generated by Django 5.0.3 on 2024-04-16 10:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
        ('envapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='envapp.environment'),
        ),
        migrations.AddField(
            model_name='application',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications_as_to_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications_as_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
