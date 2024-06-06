from django import forms
from .models import MechanicSchedule


from django import forms
from .models import MechanicSchedule


class MechanicScheduleForm(forms.ModelForm):
    class Meta:
        model = MechanicSchedule
        fields = ['date', 'shift', 'mechanic']


