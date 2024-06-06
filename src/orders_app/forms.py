from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Order, OrderSpecification
from ..car_app.models import Car
from ..services_app.models import Service


class OrderForm(forms.ModelForm):
    TIME_CHOICES = [(f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
                    for hour in range(9, 20) for minute in range(0, 60, 30)]

    chosen_time = forms.ChoiceField(label='Выберите время', choices=TIME_CHOICES)

    class Meta:
        model = Order
        exclude = ['manager', 'end_date', 'end_time', 'final_cost', 'status_choices', 'status', 'desired_service']
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


class OrderSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)


class OrderFormManager(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['chosen_date', 'chosen_time', 'desired_service', 'comment', 'car', 'status', 'manager', 'final_cost',
                  'end_date', 'end_time']

    car = forms.ModelChoiceField(queryset=Car.objects.none(), label='Автомобиль')

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
        if client:
            self.fields['car'].queryset = Car.objects.filter(client=client)
        else:
            self.fields['car'].queryset = Car.objects.all()


class OrderSpecificationForm(forms.ModelForm):
    class Meta:
        model = OrderSpecification
        fields = ['mechanic', 'service']

    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Услуга')


OrderSpecificationFormSet = inlineformset_factory(Order, OrderSpecification, form=OrderSpecificationForm, extra=1)
