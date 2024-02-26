from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .views import welcome_page_client

urlpatterns = [
    path('registration/', views.registration, name='registration'),  # Маршрут для страницы регистрации
    path('login/', views.login_user, name='login'),  # Маршрут для страницы авторизации
    path('logout/', views.logout_view,  name='logout'),
    path('home/', login_required(welcome_page_client), name='welcome_page'),

    path('personal-login', views.custom_login, name='personal-login'),

    # path('manager-login/', views.login_manager, name='manager_login'),

    # path('mechanic-login/', views.login_mechanic, name='mechanic_login'),
]
