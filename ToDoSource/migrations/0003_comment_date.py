# Generated by Django 5.0.3 on 2024-04-02 09:20

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoSource', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
