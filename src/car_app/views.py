from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddCarForm, UpdateCarForm, CarSearchForm
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
    return render(request, '../templates/сars/add_car.html', {'form': form})


@login_required
def delete_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        return redirect('garage')
    return render(request, '../templates/сars/delete_car.html', {'car_id': car_id})


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
    return render(request, '../templates/сars/update_car.html', {'form': form})


@login_required
def garage_view(request):
    cars = Car.objects.filter(client=request.user)
    return render(request, '../templates/сars/garage.html', {'cars': cars})


@login_required
def car_list_view(request):
    form = CarSearchForm(request.GET)
    cars = Car.objects.filter(client=request.user)

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            cars = cars.filter(
                Q(sts__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(model__icontains=search_query) |
                Q(body_type__icontains=search_query) |
                Q(license_plate__icontains=search_query) |
                Q(color__icontains=search_query) |
                Q(vin_number__icontains=search_query) |
                Q(year_of_manufacture__icontains=search_query)
            )

    return render(request, '../templates/сars/garage.html', {'form': form, 'cars': cars})


