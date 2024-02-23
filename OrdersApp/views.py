from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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


@login_required
def all_appeals_view(request):
    appeals = Appeal.objects.all()
    return render(request, 'all_appeals.html', {'appeals': appeals})


@login_required
def appeal_details(request, appeal_id):
    appeal = get_object_or_404(Appeal, pk=appeal_id)
    return render(request, 'appeal_details.html', {'appeal': appeal})
