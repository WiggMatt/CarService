from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.registration, name='registration'),  # Маршрут для страницы регистрации
    path('login/', views.login_user, name='login'),  # Маршрут для страницы авторизации
    path('logout/', views.logout_view,  name='logout'),
    path('personal-login', views.custom_login, name='personal-login'),
    path('personal-check/', views.personal_check, name='personal_check'),  # Маршрут для персональной страницы
]
