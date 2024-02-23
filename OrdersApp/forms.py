from datetime import datetime

from django import forms
from .models import Appeal


class AppealForm(forms.ModelForm):
    TIME_CHOICES = [(f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
                    for hour in range(9, 20) for minute in range(0, 60, 30)]

    chosen_time = forms.ChoiceField(label='Выберите время', choices=TIME_CHOICES)

    class Meta:
        model = Appeal
        exclude = ['manager']
        widgets = {
            'chosen_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        cars = kwargs.pop('cars', None)
        super().__init__(*args, **kwargs)
        if user and cars:
            self.fields['car'].queryset = cars
