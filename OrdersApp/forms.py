from django import forms
from django.utils import timezone
from .models import Appeal


class AppealForm(forms.ModelForm):
    TIME_CHOICES = [(f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
                    for hour in range(9, 20) for minute in range(0, 60, 30)]

    chosen_time = forms.ChoiceField(label='Выберите время', choices=TIME_CHOICES)

    class Meta:
        model = Appeal
        exclude = ['manager', 'is_processed']
        widgets = {
            'chosen_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        cars = kwargs.pop('cars', None)
        super().__init__(*args, **kwargs)
        if user and cars:
            self.fields['car'].queryset = cars

        self.fields['chosen_date'].label = 'Выберите дату'
        self.fields['comment'].label = 'Комментарий'
        self.fields['car'].label = 'Выберите автомобиль'

    def clean_chosen_date(self):
        chosen_date = self.cleaned_data['chosen_date']
        if chosen_date < timezone.now().date():
            raise forms.ValidationError("Вы не можете выбирать дату в прошлом")
        return chosen_date
