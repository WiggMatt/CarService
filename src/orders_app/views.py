from datetime import datetime, date

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, Spacer, SimpleDocTemplate, Paragraph, TableStyle

from src.users_app.models import Mechanic, Manager, CustomUser, Client
from src.car_app.models import Car, Recommendation
from src.services_app.models import Service
from .forms import OrderForm
from .models import Order
from ..car_app.forms import AddCarForm
from ..users_app.forms import RegistrationForm


# ////////////////////////// Для клиента //////////////////////////////
@login_required
def create_order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_order')
    else:
        user_cars = Car.objects.filter(client=request.user)
        form = OrderForm(user=request.user, cars=user_cars)
    return render(request, '../templates/orders/create_order.html', {'form': form})


@login_required
def client_order_view(request):
    client = request.user
    client_orders = Order.objects.filter(car__client=client).exclude(status='COMPLETED')

    return render(request, '../templates/orders/client_order.html', {
        'client_orders': client_orders,
    })


@login_required
def order_history_view(request):
    user = request.user
    # Получаем все завершенные заказы для автомобилей текущего клиента
    client_orders = Order.objects.filter(car__client=user, status='COMPLETED').order_by('-created_at')

    return render(request, '../templates/orders/service_history.html', {'client_orders': client_orders})


# ////////////////////////// Для менеджера //////////////////////////////
def generate_work_order_pdf(request, order_id):
    # Register a TTF font to support Russian characters
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'fonts/DejaVu/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'fonts/DejaVu/DejaVuSans-Bold.ttf'))
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_form.pdf"'

    # Create the PDF object, using the response object as its "file"
    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=12 * mm, leftMargin=12 * mm, topMargin=12 * mm,
                            bottomMargin=12 * mm)

    # Container for the 'Flowable' objects
    elements = []

    # Sample styles
    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(name='Normal', parent=styles['Normal'], fontName='DejaVuSans', fontSize=10)
    styleH = ParagraphStyle(name='Heading1', parent=styles['Heading1'], fontName='DejaVuSans', fontSize=12,
                            spaceAfter=6)
    styleB = ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='DejaVuSans-Bold', fontSize=10)

    # Add title and header information
    elements.append(Paragraph("Заказ-наряд AA-000008", styleH))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Дата приема заказа: 13.09.2023", styleN))
    elements.append(Paragraph("Дата выполнения заказа: 13.09.2023", styleN))
    elements.append(Paragraph("№ гарантийного талона: ", styleN))
    elements.append(Paragraph("Заказ принял: Николай", styleN))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Исполнитель", styleH))
    elements.append(Paragraph("Автосервис", styleN))
    elements.append(Paragraph("Ул. Ленина, 60", styleN))
    elements.append(Paragraph("ИНН: ", styleN))
    elements.append(Paragraph("Контактный телефон: ", styleN))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Заказчик", styleH))
    elements.append(Paragraph("Иванов Иван", styleN))
    elements.append(Paragraph("Тел. +70000000001", styleN))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Детали автомобиля", styleH))

    # Add car details
    car_details = [
        ["Марка", "BMW", "Гос. номер", "123"],
        ["Модель", "E 34", "Номер кузова", ""],
        ["Год выпуска", "1995", "Номер двигателя", ""],
        ["VIN", "", "Описание дефектов / комментарий", ""],
    ]
    table = Table(car_details, colWidths=[30 * mm, 40 * mm, 30 * mm, 60 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Работы", styleH))

    # Add work details
    work_details = [
        ["№", "Код", "Наименование работ", "Количество", "Цена, руб", "Сумма, руб", "Исполнитель", "Подпись"],
        ["1", "61", "Диагностика ABS", "1", "1 500,00", "1 500,00", "Николай", ""],
        ["2", "60", "Замена задних колодок", "1", "3 000,00", "3 000,00", "Николай", ""],
        ["3", "58", "Замена свечей зажигания", "1", "2 000,00", "2 000,00", "Николай", ""],
        ["4", "59", "Масло АКПП проверка, корректировка", "1", "2 000,00", "2 000,00", "Николай", ""],
    ]
    table = Table(work_details, colWidths=[8 * mm, 10 * mm, 50 * mm, 15 * mm, 20 * mm, 20 * mm, 25 * mm, 20 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Материалы исполнителя", styleH))

    # Add materials of executer
    materials_exec = [
        ["№", "Код", "Наименование материала", "Количество", "Цена, руб", "Сумма, руб"],
        ["1", "63", "Масло моторное синтетическое 3.1л BMW", "1 шт", "2 500,00", "2 500,00"],
        ["2", "62", "Свечи зажигания IRIDIUM", "6 шт", "1 500,00", "9 000,00"],
    ]
    table = Table(materials_exec, colWidths=[8 * mm, 10 * mm, 70 * mm, 15 * mm, 20 * mm, 20 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Материалы заказчика", styleH))

    # Add materials of customer
    materials_customer = [
        ["Наименование материала", "Количество"],
        ["колодки", "2"],
    ]
    table = Table(materials_customer, colWidths=[80 * mm, 40 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Итого, за работы и материалы, руб 20 000,00", styleN))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Заказ и замененные дефектные детали (остатки материалов) получены. Изделие проверено в моем присутствии.",
        styleN))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Дата _____________________________ Подпись заказчика / __________________________________ Подпись исполнителя / __________________________________",
        styleN))

    # Build the PDF
    doc.build(elements)

    return response


@login_required
def manager_orders_view(request):
    search_query = request.GET.get('search_query')
    search_date = request.GET.get('search_date')
    orders = Order.objects.all()

    if search_query:
        orders = orders.filter(
            Q(created_at__icontains=search_query) |
            Q(chosen_date__icontains=search_query) |
            Q(chosen_time__icontains=search_query) |
            Q(car__brand__icontains=search_query) |
            Q(car__model__icontains=search_query) |
            Q(car__license_plate__icontains=search_query) |
            Q(car__client__bio__icontains=search_query)
        )

    if search_date:
        try:
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
        except ValueError:
            search_date = None

        if search_date:
            orders = orders.filter(chosen_date=search_date)

    return render(request, 'orders/manager_orders.html', {'orders': orders})



@csrf_exempt
def order_details_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    services = Service.objects.all()
    mechanics = Mechanic.objects.all()
    order_specifications = order.orderspecification_set.all()
    recommendations = order.car.recommendations.all()

    if request.method == 'POST':
        if request.POST.get('action') == 'change_status':
            new_status = request.POST.get('new_status')
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'message': 'Статус заказа обновлен'})

        elif request.POST.get('action') == 'add_service':
            service_id = request.POST.get('service_id')
            mechanic_id = request.POST.get('mechanic_id')
            service = get_object_or_404(Service, id=service_id)
            mechanic = get_object_or_404(Mechanic, id=mechanic_id)
            order.orderspecification_set.create(service=service, mechanic=mechanic)

            # If the order is in progress, allow adding recommendations
            if order.status == 'IN_PROGRESS':
                return JsonResponse({'success': True, 'message': 'Услуга добавлена', 'allow_recommendations': True})
            else:
                return JsonResponse({'success': True, 'message': 'Услуга добавлена', 'allow_recommendations': False})

        elif request.POST.get('action') == 'add_recommendation':
            service_id = request.POST.get('service_id')
            comment = request.POST.get('comment')
            date = request.POST.get('date')

            service = None
            if service_id:
                service = get_object_or_404(Service, id=service_id)

            Recommendation.objects.create(
                car=order.car,
                service=service,
                comment=comment,
                date=date
            )
            return JsonResponse({'success': True, 'message': 'Рекомендация добавлена'})

    return render(request, '../templates/orders/order_details.html', {
        'order': order,
        'services': services,
        'mechanics': mechanics,
        'order_specifications': order_specifications,
        'recommendations': recommendations,
    })


@login_required
def register_client_and_car_view(request):
    message = None
    clients = CustomUser.objects.filter(is_client=True)
    client_form = RegistrationForm()  # Перемещаем определение переменной сюда
    if request.method == 'POST':
        register_car_only = request.POST.get('register_car_only', False)
        if register_car_only:
            selected_client_id = request.POST.get('client', None)
            if selected_client_id:
                client = CustomUser.objects.get(id=selected_client_id)
                car_form = AddCarForm(request.POST)
                if car_form.is_valid():
                    car = car_form.save(commit=False)
                    car.client = client
                    car.save()
                    message = "Car registration successful!"
            else:
                message = "Please select a client."
        else:
            client_form = RegistrationForm(
                request.POST)  # Перемещаем сюда для учета регистрации клиента, если не выбран только режим регистрации автомобиля
            car_form = AddCarForm(request.POST)
            if client_form.is_valid() and car_form.is_valid():
                client = client_form.save(commit=False)
                client.is_client = True
                client.save()
                car = car_form.save(commit=False)
                car.client = client
                car.save()
                message = "Client and car registration successful!"
    else:
        car_form = AddCarForm()
    return render(request, '../templates/orders/reg_client_and_car.html',
                  {'client_form': client_form, 'car_form': car_form, 'message': message, 'clients': clients})


def create_order_by_manager_view(request):
    clients = Client.objects.all()
    mechanics = Mechanic.objects.none()
    allowed_statuses = [
        ('PENDING', 'Ожидает выполнения'),
        ('IN_PROGRESS', 'В процессе выполнения'),
        ('WAITING_CAR', 'Ожидает автомобиля')
    ]
    time_choices = [(f"{hour:02d}:{minute:02d}", f"{hour:02d}:{minute:02d}")
                    for hour in range(9, 21) for minute in range(0, 60, 30)]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        if 'client_id' in request.GET:
            client_id = request.GET.get('client_id')
            cars = Car.objects.filter(client_id=client_id)
            car_list = [{'id': car.id, 'brand': car.brand, 'model': car.model,
                         'license_plate': car.license_plate} for car in cars]
            return JsonResponse(car_list, safe=False)

    if request.method == 'POST':
        chosen_date = request.POST.get('chosen_date')
        chosen_time = request.POST.get('chosen_time')
        comment = request.POST.get('comment')
        status = request.POST.get('status')
        car_id = request.POST.get('car_id')
        user = request.user

        # Fetch the Manager instance associated with the current user
        manager = get_object_or_404(Manager, id=user.id)

        Order.objects.create(
            car=get_object_or_404(Car, id=car_id),
            chosen_date=chosen_date,
            chosen_time=chosen_time,
            comment=comment,
            status=status,
            manager=manager,  # Correctly assign the Manager instance
        )

        return redirect('manager_orders')

    return render(request, '../templates/orders/create_order_by_manager.html', {
        'clients': clients,
        'mechanics': mechanics,
        'statuses': allowed_statuses,
        'time_choices': time_choices,
        'today': date.today().isoformat()
    })
