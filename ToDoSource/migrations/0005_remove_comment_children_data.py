# Generated by Django 5.0.3 on 2024-04-03 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoSource', '0004_remove_comment_parent_id_comment_children_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='children_data',
        ),
    ]