from .util import render, redirect, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from ..forms import LoginForm


def login_page(request):
    '''
    Страница авторизации

    :param request: запрос клиента
    :return: страница авторизации
    :rtype: HttpResponse
    '''

    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.data['username']
            password = loginform.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(
                    request, messages.SUCCESS, 'Авторизация успешна')
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Неправильный логин или пароль')
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Некорректные данные в форме авторизации')
            return redirect('login')
    else:
        return render(request, 'login.html', {'form': LoginForm()})


def register_page(request):
    '''
    Страница регистрации

    :param request: запрос клиента
    :return: страница регистрации
    :rtype: HttpResponse
    '''

    if request.method == 'POST':
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            regform.save()
            username = regform.data['username']
            password = regform.data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(
                    request, messages.SUCCESS, 'Регистрация успешна')
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Ошибка регистрации')
                return redirect('register')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Некорректные данные')
            return redirect('register')
    else:
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'register.html', context)


@login_required
def logout_page(request):
    '''
    Страница выхода из профиля

    :param request: запрос клиента
    :return: редирект на стартовую страницу
    :rtype: HttpResponse
    '''

    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         "Вы успешно вышли из аккаунта")
    return redirect('index')
