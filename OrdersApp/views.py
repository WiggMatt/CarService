from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from AuthenticationApp.models import Mechanic
from CarApp.models import Car
from .forms import AppealForm
from .models import Appeal, Order


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


@login_required
def all_appeals_view(request):
    appeals = Appeal.objects.all()
    return render(request, 'all_appeals.html', {'appeals': appeals})


@login_required
def appeal_details(request, appeal_id):
    appeal = get_object_or_404(Appeal, pk=appeal_id)
    mechanics = Mechanic.objects.all()
    return render(request, 'appeal_details.html', {'appeal': appeal, 'mechanics': mechanics})


def update_appeal(request, appeal_id=None):
    if request.method == 'POST':
        # Получите данные из POST-запроса
        new_date = request.POST.get('newDate')
        new_time = request.POST.get('newTime')
        mechanic_id = request.POST.get('mechanic')

        # Обновите данные в базе данных
        appeal = Appeal.objects.get(pk=appeal_id)
        appeal.chosen_date = new_date
        appeal.chosen_time = new_time
        appeal.manager = request.manager  # Предполагается, что менеджер авторизован
        appeal.is_processed = True
        appeal.save()

        # Создайте заказ на обслуживание
        mechanic = Mechanic.objects.get(pk=mechanic_id)
        order = Order.objects.create(
            car=appeal.car,
            start_date=new_date,
            start_time=new_time,
            appeal=appeal,
            # Добавьте остальные поля заказа по вашим требованиям
        )

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'})