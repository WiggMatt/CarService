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
            return redirect('welcome_page')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def welcome_page_client(request):
    return render(request, 'welcome_page.html', {"title": "Welcome Page"})


def logout_view(request):
    logout(request)
    return redirect('login')


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
                return redirect(request.GET.get('next', 'welcome_page'))
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
