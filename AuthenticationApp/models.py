from django.contrib.auth.models import AbstractUser
from django.db import models


class Client(AbstractUser):
    username = models.EmailField("Электронная почта", max_length=100, unique=True)
    bio = models.CharField("ФИО", max_length=100)
    phone_number = models.CharField("Номер телефона", max_length=11, unique=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
