# Generated by Django 5.0.2 on 2024-04-07 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoSource', '0008_alter_environment_password_alter_task_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='is_superadmin',
            field=models.BooleanField(default=False),
        ),
    ]
