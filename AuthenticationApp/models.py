from django.contrib.auth.models import AbstractUser
from django.db import models

from ServiceApp.models import Service


class CustomUser(AbstractUser):
    username = models.EmailField("Электронная почта", max_length=100, unique=True)
    bio = models.CharField("ФИО", max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=18, unique=True)

    REQUIRED_FIELDS = ["bio", "phone_number"]

    def __str__(self):
        return self.bio


class Administrator(CustomUser):
    license_num = models.CharField("Номер ВУ", max_length=12, unique=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Client(CustomUser):
    license_num = models.CharField("Номер ВУ", max_length=12, unique=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Manager(CustomUser):
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'


class Mechanic(CustomUser):
    class Meta:
        verbose_name = 'Механик'
        verbose_name_plural = 'Механики'


class MechanicSpecialization(models.Model):
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE, verbose_name='Механик')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')

    class Meta:
        verbose_name = 'Спецификация механика'
        verbose_name_plural = 'Спецификации механиков'
