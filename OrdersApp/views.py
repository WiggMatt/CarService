from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from CarApp.models import Car
from .forms import AppealForm
from .models import Appeal


@login_required
def create_appeal(request):
    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            form.save()
            # Перенаправление пользователя после успешного создания заявки
            return redirect('appeals_view')
    else:
        user_cars = Car.objects.filter(client=request.user)
        form = AppealForm(user=request.user, cars=user_cars)
    return render(request, 'create_appeal.html', {'form': form})


@login_required
def appeals_view(request):
    client_appeals = Appeal.objects.filter(car_id__client=request.user)
    return render(request, 'appeals_view.html', {'appeals': client_appeals})
