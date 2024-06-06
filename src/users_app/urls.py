from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.client_registration_view, name='registration'),
    path('login/', views.client_login_view, name='login'),
    path('logout/', views.logout_view,  name='logout'),
    path('personal-login', views.manager_login_view, name='personal-login'),
    path('personal-check/', views.personal_check, name='personal_check'),
]
