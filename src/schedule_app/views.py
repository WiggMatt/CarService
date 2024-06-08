from django.shortcuts import render, redirect

from .forms import MechanicScheduleForm
from .models import MechanicSchedule, Shift


def manage_schedule(request):
    if request.method == 'POST':
        schedule_form = MechanicScheduleForm(request.POST, prefix='schedule')

        if schedule_form.is_valid():
            schedule_form.save()
            return redirect('manage_schedule')
    else:
        schedule_form = MechanicScheduleForm(prefix='schedule')

    shifts = Shift.objects.all()
    schedules = MechanicSchedule.objects.all()

    return render(request, '../templates/schedule/mechanic_schedule_list.html', {
        'schedule_form': schedule_form,
        'shifts': shifts,
        'schedules': schedules
    })