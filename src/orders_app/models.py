from datetime import datetime

from django.db import models

from src.users_app.models import Manager, Mechanic
from src.car_app.models import Car
from src.services_app.models import Service


class OrderSpecification(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, verbose_name='Механик')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')

    class Meta:
        verbose_name = 'Спецификация заказа'
        verbose_name_plural = 'Спецификации заказов'

    def __str__(self):
        return f"Спецификация для заказа {self.order} - {self.service} у механика {self.mechanic}"


class Order(models.Model):
    created_at = models.DateTimeField("Дата создания заявки", auto_now_add=True)
    chosen_date = models.DateField("Дата выбранная пользователем")
    chosen_time = models.TimeField("Время выбранное пользователем", null=True)
    desired_service = models.CharField(max_length=150, verbose_name='Желаемая услуга', blank=True, null=True)
    comment = models.TextField("Комментарий клиента", blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    status_choices = [
        ('AWAITING_CONFIRMATION', 'Ожидает подтверждения'),
        ('PENDING', 'Ожидает выполнения'),
        ('WAITING_CAR', 'Ожидает автомобиля'),
        ('IN_PROGRESS', 'В процессе выполнения'),
        ('COMPLETED', 'Выполнен'),
    ]
    status = models.CharField(max_length=100, choices=status_choices, default='AWAITING_CONFIRMATION',
                              verbose_name='Статус выполнения')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="Идентификатор менеджера",
                                blank=True, null=True)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Конечная стоимость', blank=True,
                                     null=True)
    end_date = models.DateField(verbose_name='Дата окончания выполнения', blank=True, null=True)
    end_time = models.TimeField(verbose_name='Время окончания выполнения', blank=True, null=True)

    def __str__(self):
        return f"Заказ для {self.car}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
