from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
<<<<<<< HEAD
#models
from .models import TrackSettings, TrackComment, MusicTrack, Profile
#forms
from django.contrib.auth.forms import UserCreationForm
=======

>>>>>>> develop
from .forms import LoginForm
from django.contrib.auth.forms import UserCreationForm


def get_base_context(request):
    '''
    Возвращает базовый контекст для всех страниц сайта
    
    :param request: запрос клиента
    :return: словарь контекста
    '''

    return {
        'user': request.user
    }


def index(request):
    '''
    Главная страница

    :param request: запрос клиента
    :return: главная страница
    :rtype: HttpResponse
    '''

    return render(request, 'index.html', get_base_context(request))


def editor(request):
    '''
    Страница редактора мелодии

    :param request: запрос клиента
    :return: страница редактора мелодии
    :rtype: HttpResponse
    '''

    return render(request, 'editor.html', get_base_context(request))


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
                messages.add_message(request, messages.SUCCESS, "Авторизация успешна")
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, "Неправильный логин или пароль")
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме авторизации")
            return redirect('login')
    else:
        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)


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
                messages.add_message(request, messages.SUCCESS, "Регистрация успешна")
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, "Ошибка регистрации")
                return redirect('register')
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные")
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
    messages.add_message(request, messages.SUCCESS, "Вы успешно вышли из аккаунта")
    return redirect('index')


@login_required
def profile_page(request):
    all_tracks = MusicTrack.objects.all()
    profile = Profile.objects.all()
    context = {
        "request": request,
        "user": request.user,
        "tracks": all_tracks.filter(author=request.user),
        "likes": all_tracks.filter(likes=request.user),
    }
    return render(request, 'profile.html', context)