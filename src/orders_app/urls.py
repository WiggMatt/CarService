from django.urls import path
from . import views

urlpatterns = [
    # Для клиента
    path('appeals/', views.appeals_view, name='appeals_view'),
    path('appeals/create_appeal/', views.create_appeal, name='create_appeal'),
    path('appeals/history/', views.appeals_history, name='appeals_history'),

    # Для менеджера
    path('all-appeals/', views.all_appeals_view, name='all_appeals'),
    path('appeal/<int:appeal_id>/', views.appeal_details, name='appeal_details'),
    path('update_appeal/<int:appeal_id>/', views.update_appeal, name='update_appeal'),
    path('all-appeals/search/', views.appeal_list, name='appeal_list'),
    path('all-orders/', views.all_orders_view, name='all_orders'),
    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
]
