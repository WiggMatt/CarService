# Generated by Django 5.0.2 on 2024-02-23 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0003_alter_order_final_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='start_time',
        ),
    ]
