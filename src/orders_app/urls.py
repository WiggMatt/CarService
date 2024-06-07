from django.urls import path
from . import views

urlpatterns = [
    # Для клиента
    path('appeals/', views.client_order_view, name='client_order'),
    path('appeals/create_appeal/', views.create_order_view, name='create_order'),
    path('appeals/history/', views.order_history_view, name='orders_history'),

    # Для менеджера
    path('orders/', views.manager_orders_view, name='manager_orders'),
    path('orders/<int:order_id>/', views.order_details_view, name='order_details'),
    # path('orders/search/', views.orders_search_view, name='orders_search'),
    path('generate_work_order_pdf/<int:order_id>/', views.generate_work_order_pdf, name='generate_work_order_pdf'),
    path('register-client-and-car/', views.register_client_and_car_view, name='register_client_and_car'),
    path('create-order/', views.create_order_by_manager_view, name='create_order_by_manager'),
]
