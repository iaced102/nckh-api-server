# Generated by Django 3.2.18 on 2023-05-23 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_remove_sessions_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='note',
            field=models.TextField(default=''),
        ),
    ]