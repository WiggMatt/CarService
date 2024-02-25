from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from AuthenticationApp.forms import RegistrationForm, LoginForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticate_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, authenticate_user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def welcome_page_client(request):
    return render(request, 'client_page.html', {"title": "Welcome Page"})


def logout_view(request):
    logout(request)
    return redirect('main_page')


def main_view(request):
    return render(request, 'home_page.html')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Редирект на страницу, куда пользователь хотел попасть перед авторизацией
                return redirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def login_manager(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Редирект на страницу, куда пользователь хотел попасть перед авторизацией
                return redirect(request.GET.get('next', 'all_appeals'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def login_mechanic(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Редирект на страницу, куда пользователь хотел попасть перед авторизацией
                return redirect(request.GET.get('next', 'all_orders'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

