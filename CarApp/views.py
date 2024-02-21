from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCarForm, UpdateCarForm
from .models import Car


@login_required
def add_car_view(request):
    if request.method == 'POST':
        form = AddCarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.client = request.user  # Привязываем автомобиль к текущему пользователю
            car.save()
            return redirect('garage')
    else:
        form = AddCarForm(initial={'client': request.user})  # Устанавливаем значение клиента в форме
    return render(request, 'add_car.html', {'form': form})


@login_required
def delete_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        return redirect('garage')
    return render(request, 'delete_car.html', {'car_id': car_id})


@login_required
def update_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = UpdateCarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('garage')  # Предполагается, что у вас есть url с именем 'home'
    else:
        form = UpdateCarForm(instance=car)
    return render(request, 'update_car.html', {'form': form})


@login_required
def garage_view(request):
    cars = Car.objects.filter(client=request.user)
    return render(request, 'garage.html', {'cars': cars})
