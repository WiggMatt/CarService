from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect


from src.users_app.forms import RegistrationForm, LoginForm


def client_registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticate_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request, authenticate_user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, '../templates/users/registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main_page')


def main_view(request):
    return render(request, '../templates/users/home_page.html')


def client_login_view(request):
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
    return render(request, '../templates/users/login.html', {'form': form})


def manager_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('manager_orders')
    else:
        form = LoginForm()
    return render(request, '../templates/users/personal_login.html', {'form': form})


def personal_check(request):
    if request.user.is_manager:
        return redirect('manager_orders')



