# Generated by Django 5.0.2 on 2024-04-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='title',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]