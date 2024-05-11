from django.db import models

from src.services_app.models import Service
from src.users_app.models import Client, CustomUser


class Car(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sts = models.CharField("СТС", max_length=100)
    brand = models.CharField("Марка", max_length=100)
    model = models.CharField("Модель", max_length=100)
    body_type = models.CharField("Тип кузова", max_length=100)
    license_plate = models.CharField("Государственный номер", max_length=20)
    color = models.CharField("Цвет", max_length=50)
    vin_number = models.CharField("VIN номер", max_length=100)
    year_of_manufacture = models.PositiveSmallIntegerField("Год выпуска")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"


class Recommendation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='recommendations', verbose_name='Автомобиль')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='recommendations',
                                verbose_name='Услуга', null=True)
    comment = models.CharField(verbose_name='Комментарий', max_length=200)
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'

    def __str__(self):
        return f'{self.comment} - {self.date} - {self.service}'
