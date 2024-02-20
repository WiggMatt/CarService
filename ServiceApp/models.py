from django.db import models


class ServiceGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название группы услуг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа услуг'
        verbose_name_plural = 'Группы услуг'


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    price_range = models.CharField(max_length=100, verbose_name='Стоимость')
    duration = models.CharField(max_length=100, verbose_name='Примерное время выполнения')
    service_group = models.ForeignKey('ServiceGroup', on_delete=models.CASCADE, verbose_name='Группа услуг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'