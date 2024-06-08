from django.urls import path
from . import views

urlpatterns = [
    path('garage/', views.garage_view, name='garage'),
    path('garage/delete_car/<int:car_id>/', views.delete_car_view, name='delete_car'),
    path('garage/update_car/<int:car_id>/', views.update_car_view, name='update_car'),
]
