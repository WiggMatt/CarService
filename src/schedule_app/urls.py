from django.urls import path
from . import views

urlpatterns = [
    path('manage_schedule/', views.manage_schedule, name='manage_schedule'),
]