from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import AddCarForm, UpdateCarForm
from .models import Car


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
@require_http_methods(["GET", "POST"])
def garage_view(request):
    if request.method == 'POST':
        if 'car_id' in request.POST:
            car_id = request.POST.get('car_id')
            car = get_object_or_404(Car, id=car_id, client=request.user)
            form = AddCarForm(request.POST, instance=car)
            if form.is_valid():
                form.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': 'Информация об автомобиле обновлена успешно!'})
                return redirect('garage')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
        else:
            form = AddCarForm(request.POST)
            if form.is_valid():
                car = form.save(commit=False)
                car.client = request.user
                car.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': 'Автомобиль добавлен успешно!'})
                return redirect('garage')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)

    search_query = request.GET.get('search_query')
    cars = Car.objects.filter(client=request.user)

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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'car_id' in request.GET:
        car_id = request.GET.get('car_id')
        car = get_object_or_404(Car, id=car_id, client=request.user)
        car_data = {
            'id': car.id,
            'sts': car.sts,
            'brand': car.brand,
            'model': car.model,
            'body_type': car.body_type,
            'license_plate': car.license_plate,
            'color': car.color,
            'vin_number': car.vin_number,
            'year_of_manufacture': car.year_of_manufacture,
        }
        return JsonResponse(car_data)

    return render(request, '../templates/сars/garage.html', {'cars': cars})

