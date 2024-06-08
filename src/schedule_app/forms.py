from django import forms
from .models import MechanicSchedule, Shift

from django import forms
from .models import MechanicSchedule


class MechanicScheduleForm(forms.ModelForm):
    class Meta:
        model = MechanicSchedule
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'mechanic': forms.Select(attrs={'class': 'select2'})
        }

