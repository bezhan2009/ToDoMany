# Generated by Django 5.0.3 on 2024-04-16 10:00

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('envapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
                ('money', models.IntegerField(default=0)),
                ('deadline', models.DateTimeField(blank=True, default=1, null=True)),
                ('environment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='envapp.environment')),
            ],
        ),
    ]
