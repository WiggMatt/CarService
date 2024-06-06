from django.http import JsonResponse
from django.shortcuts import render

from .forms import MechanicScheduleForm
from .models import MechanicSchedule, Shift
from ..users_app.models import Mechanic


def schedule_view(request):
    mechanics = Mechanic.objects.all()
    shifts = Shift.objects.all()
    schedules = MechanicSchedule.objects.all()
    return render(request, '../templates/schedule/mechanic_schedule_list.html', {'mechanics': mechanics, 'shifts': shifts, 'schedules': schedules})

def add_schedule(request):
    if request.method == 'POST':
        form = MechanicScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = MechanicScheduleForm()
    return render(request, '../templates/schedule/mechanic_schedule_list.html', {'form': form})
