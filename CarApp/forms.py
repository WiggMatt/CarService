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
