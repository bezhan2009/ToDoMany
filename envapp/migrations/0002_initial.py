# Generated by Django 5.0.3 on 2024-04-16 10:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('envapp', '0001_initial'),
        ('userapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='environment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.userprofile'),
        ),
        migrations.AddField(
            model_name='savedenvironment',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='envapp.environment'),
        ),
        migrations.AddField(
            model_name='savedenvironment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]