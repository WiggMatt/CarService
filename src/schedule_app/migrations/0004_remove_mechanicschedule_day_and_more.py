# Generated by Django 5.0.2 on 2024-05-18 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule_app', '0003_remove_mechanicschedule_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mechanicschedule',
            name='day',
        ),
        migrations.RemoveField(
            model_name='mechanicschedule',
            name='week',
        ),
    ]
