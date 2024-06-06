# Generated by Django 5.0.2 on 2024-05-16 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders_app', '0001_initial'),
        ('services_app', '0001_initial'),
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users_app.manager', verbose_name='Идентификатор менеджера'),
        ),
        migrations.AddField(
            model_name='orderspecification',
            name='mechanic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.mechanic', verbose_name='Механик'),
        ),
        migrations.AddField(
            model_name='orderspecification',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders_app.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='orderspecification',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services_app.service', verbose_name='Услуга'),
        ),
    ]
