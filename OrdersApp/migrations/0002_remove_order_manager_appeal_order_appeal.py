# Generated by Django 5.0.2 on 2024-02-21 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationApp', '0001_initial'),
        ('CarApp', '0001_initial'),
        ('OrdersApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='manager',
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заявки')),
                ('chosen_date', models.DateField(verbose_name='Дата выбранная пользователем')),
                ('chosen_time', models.TimeField(verbose_name='Время выбранное пользователем')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий клиента')),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CarApp.car', verbose_name='Идентификатор авто')),
                ('manager_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='AuthenticationApp.manager', verbose_name='Идентификатор менеджера')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='appeal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='OrdersApp.appeal', verbose_name='Заявка'),
        ),
    ]