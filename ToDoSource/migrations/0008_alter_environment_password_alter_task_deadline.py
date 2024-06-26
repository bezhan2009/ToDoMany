# Generated by Django 5.0.2 on 2024-04-07 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoSource', '0007_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, default=1, null=True),
        ),
    ]
