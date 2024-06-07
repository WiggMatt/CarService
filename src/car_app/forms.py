from django import forms
from .models import Car


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['sts', 'brand', 'model', 'body_type', 'license_plate', 'color', 'vin_number', 'year_of_manufacture']


class DeleteCarForm(forms.Form):
    car_id = forms.IntegerField(widget=forms.HiddenInput)


class UpdateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['sts', 'brand', 'model', 'body_type', 'license_plate', 'color', 'vin_number', 'year_of_manufacture']
        widgets = {
            'sts': forms.TextInput(attrs={'placeholder': 'СТС'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Марка'}),
            'model': forms.TextInput(attrs={'placeholder': 'Модель'}),
            'body_type': forms.TextInput(attrs={'placeholder': 'Тип кузова'}),
            'license_plate': forms.TextInput(attrs={'placeholder': 'Гос. номер'}),
            'color': forms.TextInput(attrs={'placeholder': 'Цвет'}),
            'vin_number': forms.TextInput(attrs={'placeholder': 'VIN номер'}),
            'year_of_manufacture': forms.NumberInput(attrs={'placeholder': 'Год выпуска'}),
        }


class CarSearchForm(forms.Form):
    search_query = forms.CharField(label='', required=False)

