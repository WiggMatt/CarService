from django.core.exceptions import ValidationError
from django.db import models

from src.users_app.models import Mechanic


class Shift(models.Model):
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift_type = models.CharField(max_length=100)

    def __str__(self):
        day_name = self.get_day_of_week_display()
        return f"{self.shift_type} shift on {day_name} from {self.start_time} to {self.end_time}"


class MechanicSchedule(models.Model):
    date = models.DateField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)

    def clean(self):
        overlapping_shifts = MechanicSchedule.objects.filter(
            date=self.date,
            mechanic=self.mechanic,
            shift__start_time__lt=self.shift.end_time,
            shift__end_time__gt=self.shift.start_time
        ).exclude(pk=self.pk)
        if overlapping_shifts.exists():
            raise ValidationError(f"{self.mechanic} is already scheduled to work during this time.")

    def __str__(self):
        return f"{self.mechanic} - {self.date} ({self.shift})"

    class Meta:
        unique_together = ('date', 'shift', 'mechanic')


