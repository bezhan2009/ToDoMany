# Generated by Django 5.0.2 on 2024-04-21 12:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]