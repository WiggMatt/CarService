from django.urls import path
from . import views

urlpatterns = [
    path('staff-schedule/', views.mechanic_schedule_list, name='mechanic_schedule_list'),
    path('staff-schedule/<int:schedule_id>/', views.mechanic_schedule_detail, name='mechanic_schedule_detail'),
    path('add-schedule/', views.add_mechanic_schedule, name='add_mechanic_schedule'),
]