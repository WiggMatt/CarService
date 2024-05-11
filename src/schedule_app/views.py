from django.shortcuts import render, redirect

from .forms import MechanicScheduleForm
from .models import MechanicSchedule


def mechanic_schedule_list(request):
    schedules = MechanicSchedule.objects.all()
    return render(request, '../templates/schedule/mechanic_schedule_list.html', {'schedules': schedules})


def mechanic_schedule_detail(request, schedule_id):
    schedule = MechanicSchedule.objects.get(id=schedule_id)
    return render(request, '../templates/schedule/mechanic_schedule_detail.html', {'schedule': schedule})


def add_mechanic_schedule(request):
    if request.method == 'POST':
        form = MechanicScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mechanic_schedule_list')
    else:
        form = MechanicScheduleForm()
    return render(request, '../templates/schedule/add_mechanic_schedule.html', {'form': form})
