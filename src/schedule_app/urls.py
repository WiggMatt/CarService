from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.schedule_view, name='schedule'),
    path('add-schedule/', views.add_schedule, name='add_schedule'),
]