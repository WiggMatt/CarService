from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from src.users_app.models import Mechanic, Manager
from src.car_app.models import Car
from src.services_app.models import Service, ServiceGroup
from .forms import AppealForm, AppealSearchForm
from .models import Appeal, Order, OrderSpecification


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
    return render(request, '../templates/orders/create_appeal.html', {'form': form})


@login_required
def appeals_view(request):
    # Получите все заявки клиента
    client_appeals = Appeal.objects.filter(car__client=request.user)

    # Создайте словарь, в котором ключами будут заявки, а значениями - соответствующие заказы
    appeal_orders = {}
    for appeal in client_appeals:
        orders = Order.objects.filter(appeal=appeal)
        appeal_orders[appeal] = orders

    return render(request, '../templates/orders/appeals_view.html', {'appeal_orders': appeal_orders})


@login_required
def all_appeals_view(request):
    appeals = Appeal.objects.all()
    return render(request, '../templates/orders/all_appeals.html', {'appeals': appeals})


@login_required
def appeal_details(request, appeal_id):
    appeal = get_object_or_404(Appeal, pk=appeal_id)
    mechanics = Mechanic.objects.all()
    return render(request, '../templates/orders/appeal_details.html', {'appeal': appeal, 'mechanics': mechanics})


@login_required
def update_appeal(request, appeal_id=None):
    if request.method == 'POST':
        # Получите данные из POST-запроса
        new_date = request.POST.get('chosenDate')
        new_time = request.POST.get('chosenTime')
        mechanic_id = request.POST.get('mechanic')

        # Получите объекты менеджера и механика
        manager = get_object_or_404(Manager, pk=request.user.pk)
        responsible_mechanic = Mechanic.objects.get(pk=mechanic_id).bio

        # Обновите данные в базе данных
        appeal = Appeal.objects.get(pk=appeal_id)
        appeal.chosen_date = new_date
        appeal.chosen_time = new_time
        appeal.manager = manager
        appeal.is_processed = True
        appeal.save()

        # Создайте заказ на обслуживание
        order = Order(
            car=appeal.car,
            appeal=appeal,
            status='PENDING',  # Устанавливаем начальный статус заказа
            name_of_the_responsible_mechanic=responsible_mechanic
        )
        order.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Метод запроса должен быть POST'})


@login_required
def all_orders_view(request):
    orders = Order.objects.all()
    return render(request, '../templates/orders/all_orders.html', {'orders': orders})


@login_required
def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    service_groups = ServiceGroup.objects.all()

    mechanic = Mechanic.objects.get(bio=order.name_of_the_responsible_mechanic)

    if request.method == 'POST':
        service_id = request.POST.get('service')
        service = Service.objects.get(id=service_id)
        order_specification = OrderSpecification.objects.create(mechanic=mechanic, service=service,
                                                                order=order)
        order_specification.save()
        return redirect('order_details', order_id=order_id)

    context = {
        'order': order,
        'service_groups': service_groups,
    }
    return render(request, '../templates/orders/order_detail.html', context)


@login_required
def update_order_status(request, order_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        order = Order.objects.get(id=order_id)

        if action == 'start_work' and order.status == 'PENDING':
            order.status = 'IN_PROGRESS'
            order.save()

        elif action == 'complete_work' and order.status == 'IN_PROGRESS':
            total_cost = order.orderspecification_set.aggregate(total_cost=Sum('service__price'))['total_cost']
            if total_cost is not None:
                order.final_cost = total_cost
            order.status = 'COMPLETED'
            order.end_date = datetime.now().date()
            order.end_time = datetime.now().time()
            order.save()

    return redirect('order_details', order_id=order_id)


@login_required
def appeals_history(request):
    # Получите все заявки клиента
    client_appeals = Appeal.objects.filter(car__client=request.user)

    # Создайте словарь, в котором ключами будут заявки, а значениями - соответствующие заказы
    appeal_orders = {}
    for appeal in client_appeals:
        orders = Order.objects.filter(appeal=appeal)
        appeal_orders[appeal] = orders

    return render(request, '../templates/orders/service_history.html', {'appeal_orders': appeal_orders})


def appeal_list(request):
    form = AppealSearchForm(request.GET)

    # Получение всех заявок
    appeals = Appeal.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        search_date = request.GET.get('search_date')  # Получение введенной даты из запроса
        if search_query:
            appeals = appeals.filter(
                Q(created_at__icontains=search_query) |
                Q(chosen_date__icontains=search_query) |
                Q(chosen_time__icontains=search_query) |
                Q(car__brand__icontains=search_query) |
                Q(car__model__icontains=search_query) |
                Q(car__license_plate__icontains=search_query) |
                Q(car__client__bio__icontains=search_query)
            )
            # Если дата указана, применяем фильтр по дате
        if search_date:
            # Попытка преобразовать строку с датой в объект datetime
            try:
                search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            except ValueError:
                search_date = None

            # Если преобразование удалось, фильтруем по выбранной дате
            if search_date:
                appeals = appeals.filter(chosen_date=search_date)

    return render(request, '../templates/orders/all_appeals.html', {'form': form, 'appeals': appeals})
