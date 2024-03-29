from django.contrib.auth.models import AbstractUser
from django.db import models

from ServiceApp.models import Service


class CustomUser(AbstractUser):
    username = models.EmailField("Электронная почта", max_length=100, unique=True)
    bio = models.CharField("ФИО", max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=18, unique=True)
    is_client = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_mechanic = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["bio", "phone_number"]

    def __str__(self):
        return self.bio

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'


class Client(CustomUser):
    license_num = models.CharField("Номер ВУ", max_length=12, unique=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def save(self, *args, **kwargs):
        self.is_client = True
        super().save(*args, **kwargs)


class Manager(CustomUser):
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def save(self, *args, **kwargs):
        self.is_manager = True
        super().save(*args, **kwargs)


class Mechanic(CustomUser):
    class Meta:
        verbose_name = 'Механик'
        verbose_name_plural = 'Механики'

    def save(self, *args, **kwargs):
        self.is_mechanic = True
        super().save(*args, **kwargs)


class MechanicSpecialization(models.Model):
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE, verbose_name='Механик')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')

    class Meta:
        verbose_name = 'Спецификация механика'
        verbose_name_plural = 'Спецификации механиков'
