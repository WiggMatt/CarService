from django.urls import path
from . import views

urlpatterns = [
    path('garage/', views.garage_view, name='garage'),
    path('garage/add_car/', views.add_car_view, name='add_car'),
    path('garage/delete_car/<int:car_id>/', views.delete_car_view, name='delete_car'),
    path('garage/update_car/<int:car_id>/', views.update_car_view, name='update_car'),
    path('garage/cars/', views.car_list_view, name='car_list'),
]
