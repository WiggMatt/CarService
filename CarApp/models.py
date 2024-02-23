from django.db import models

from AuthenticationApp.models import Client, CustomUser


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
