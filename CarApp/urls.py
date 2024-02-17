from django.urls import path
from . import views

urlpatterns = [
    path('add_car/', views.add_car_view, name='add_car'),
    path('delete_car/<int:car_id>/', views.delete_car_view, name='delete_car'),
    path('update_car/<int:car_id>/', views.update_car_view, name='update_car'),
]