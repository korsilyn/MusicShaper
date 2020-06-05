'''
=================================================
Модуль view-функций для регистрации и авторизации
=================================================
'''

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import add_message, SUCCESS, ERROR
from .util import get_base_context
from ..forms import LoginForm


def login_page(request):
    '''
    **Страница авторизации**

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
                add_message(request, SUCCESS, 'Авторизация успешна')
                return redirect('index')
            add_message(request, ERROR, 'Неправильный логин или пароль')
            return redirect('login')
        add_message(request, ERROR, 'Некорректные данные в форме авторизации')
        return redirect('login')

    context = get_base_context(request, {
        'form': LoginForm()
    })
    return render(request, 'auth/login.html', context)


def register_page(request):
    '''
    **Страница регистрации**

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
                add_message(request, SUCCESS, 'Регистрация успешна')
                return redirect('index')
            add_message(request, ERROR, 'Ошибка регистрации')
            return redirect('register')
        add_message(request, ERROR, 'Некорректные данные')
        return redirect('register')

    context = get_base_context(request, {
        'form': UserCreationForm()
    })
    return render(request, 'auth/register.html', context)


@login_required
def logout_page(request):
    '''
    **Страница выхода из профиля**

    :param request: запрос клиента
    :return: редирект на стартовую страницу
    :rtype: HttpResponse
    '''

    logout(request)
    add_message(request, SUCCESS, "Вы успешно вышли из аккаунта")
    return redirect('index')
