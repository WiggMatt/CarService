from django.db import models

from src.users_app.models import Mechanic


class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.shift_type} shift from {self.start_time} to {self.end_time}"


class MechanicSchedule(models.Model):
    date = models.DateField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, verbose_name="Идентификатор менеджера",
                                 blank=True, null=True)

    def __str__(self):
        return f"{self.mechanic}'s schedule on {self.date} for {self.shift}"
