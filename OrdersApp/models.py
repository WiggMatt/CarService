from django.db import models

from AuthenticationApp.models import Manager, Mechanic
from CarApp.models import Car
from ServiceApp.models import Service


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
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Автомобиль')
    status_choices = [
        ('PENDING', 'Ожидает выполнения'),
        ('IN_PROGRESS', 'В процессе выполнения'),
        ('COMPLETED', 'Выполнен'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='PENDING',
                              verbose_name='Статус выполнения')
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Конечная стоимость')
    creation_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    start_date = models.DateField(verbose_name='Дата начала выполнения', blank=True, null=True)
    end_date = models.DateField(verbose_name='Дата окончания выполнения', blank=True, null=True)
    start_time = models.TimeField(verbose_name='Время начала выполнения', blank=True, null=True)
    end_time = models.TimeField(verbose_name='Время окончания выполнения', blank=True, null=True)
    appeal = models.ForeignKey('Appeal', on_delete=models.SET_NULL, verbose_name='Заявка', blank=True, null=True)

    def __str__(self):
        return f"Заказ для {self.car} - {self.creation_date}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Appeal(models.Model):
    created_at = models.DateTimeField("Дата создания заявки", auto_now_add=True)
    chosen_date = models.DateField("Дата выбранная пользователем")
    chosen_time = models.TimeField("Время выбранное пользователем")
    comment = models.TextField("Комментарий клиента", blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Идентификатор авто")
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name="Идентификатор менеджера",
                                blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Заявка от {self.created_at} для авто {self.car_id}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
