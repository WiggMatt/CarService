# Generated by Django 5.0.2 on 2024-02-24 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrdersApp', '0004_remove_order_creation_date_remove_order_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='name_of_the_responsible_mechanic',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
