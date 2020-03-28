from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseBadRequest

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.core.files.base import ContentFile
from MusicShaper.settings import STATICFILES_DIRS

from django.contrib.auth.models import User
from .models import TrackSettings, TrackComment, MusicTrack, Profile, MusicTrackProject

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .forms import LoginForm

from datetime import datetime


def get_base_context(request):
    '''
    Возвращает базовый контекст для всех страниц сайта

    :param request: запрос клиента
    :return: словарь контекста
    '''

    return {
        'request': request,
        'user': request.user,
    }


def index(request):
    '''
    Главная страница

    :param request: запрос клиента
    :return: главная страница
    :rtype: HttpResponse
    '''

    return render(request, 'index.html', get_base_context(request))


@login_required
def new_project(request):
    '''
    Страница создания проекта

    :param request: запрос клиента
    :return: страница создания проекта
    :rtype: HttpResponse
    '''

    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name', '')
        desc = request.POST.get('description', '')

        if not (0 < len(name) <= 50 and 0 <= len(desc) <= 250):
            return HttpResponseBadRequest('некорректные данные формы')

        exists = MusicTrackProject.objects.filter(
            author=request.user, name=name).exists()

        if exists:
            return HttpResponseBadRequest('проект с таким названием уже существует')

        proj_instance = MusicTrackProject(
            name=name,
            desc=desc,
            author=request.user,
            creation_date=datetime.now()
        )

        proj_instance.timeline_data.save('timeline.json', ContentFile('{}'))
        proj_instance.save()

        messages.add_message(request, messages.SUCCESS,
                             'Проект успешно создан!')
        return JsonResponse({
            'proj_id': proj_instance.id
        })

    return render(request, 'project/new.html', get_base_context(request))


@login_required
def projects_list(request):
    '''
    Страница со списком проектов пользователя

    :param request: запрос клиента
    :return: список проектов
    :rtype: HttpResponse
    '''

    context = get_base_context(request)
    context['projects'] = MusicTrackProject.objects.filter(
        author=request.user).all()

    return render(request, 'project/list.html', context)


def get_project_or_404(request, id: int):
    '''
    Возвращает проект с нужным id + проверка на автора

    :param request: запрос клиента
    :param id: id проека в базе данных
    :rtype: MusicTrackProject
    '''

    project = get_object_or_404(MusicTrackProject, pk=id)
    if project.author != request.user:
        raise Http404

    return project


@login_required
def project_home(request, id: int):
    '''
    Главная страница проекта

    :param request: запрос клиента
    :param id: id проекта в базе данных
    :return: главная страница проекта
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, id)

    context = get_base_context(request)
    context['project'] = project

    return render(request, 'project/home.html', context)


@login_required
def project_instruments_list(request, id: int):
    '''
    Страница со списком всех музыкальных инструментов
    в проекте

    :param request: запрос клиента
    :param id: id проекта в базе данных
    :return: список инструментов
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, id)

    context = get_base_context(request)
    context['project'] = project
    context['instruments'] = project.instruments

    return render(request, 'project/instrument/list.html', context)


@login_required
def project_new_instrument(request, id: int):
    '''
    Страница создания музыкального инструмента

    :param request: запрос клиента
    :param id: id проекта в базе данных
    :return: страница создания инструмента
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, id)

    context = get_base_context(request)
    context['project'] = project

    with open(STATICFILES_DIRS[0] + '/data/instrumentDefaults.json', 'r', encoding='utf-8') as f:
        context['instrumentDefaults'] = f.read()

    return render(request, 'project/instrument/new.html', context)


def editor(request):
    '''
    Страница редактора мелодии

    :param request: запрос клиента
    :return: страница редактора мелодии
    :rtype: HttpResponse
    '''

    return render(request, 'project/pattern/editor.html', get_base_context(request))


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


@login_required
def profile_page(request):
    '''
    Страница профиля

    :param request: запрос клиента
    :return: страница профиля
    :rtype: HttpResponse
    '''

    username = request.GET.get('username', '')
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = get_object_or_404(Profile, user=user)

    context = get_base_context(request)
    context.update({
        "profile": profile,
        "tracks": MusicTrack.objects.filter(author=user),
        "likes": MusicTrack.objects.filter(likes=user),
    })

    return render(request, 'profile/view.html', context)


@login_required
def profile_edit_page(request):
    '''
    Страница редактирования профиля

    :param request: запрос клиента
    :return: страница редактировния профиля
    :rtype: HttpResponse
    '''

    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        status = request.POST.get('status', '')
        image = request.FILES.get('image', None)

        if len(status) <= 100:
            profile.status = status
        if image:
            profile.image.delete(save=True)
            profile.image = image

        profile.save()
        messages.add_message(request, messages.SUCCESS,
                             'Профиль успешно обновлён')
        return redirect('profile')
    else:
        context = get_base_context(request)
        context['profile'] = profile
        return render(request, 'profile/edit.html', context)


@login_required
def change_password_page(request):
    '''
    Страница смены пароля

    :param request: запрос клиента
    :return: страница смены пароля
    :rtype: HttpResponse
    '''

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.add_message(request, messages.SUCCESS,
                                 'Пароль успешно изменён')
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Некорректные данные формы')
            return redirect('change_password')
    else:
        context = get_base_context(request)
        context['form'] = PasswordChangeForm(user=request.user)
        return render(request, 'change_password.html', context)


@login_required
def profile_delete_avatar(request):
    '''
    Страница удаления аватара

    :param request: запрос клиента
    :return: страница удаления аватара
    :rtype: HttpResponse
    '''

    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        profile.image.delete(save=True)
        messages.add_message(request, messages.SUCCESS,
                             'Аватар успешно удалён')
        return redirect('profile')

    return render(request, 'profile/delete_avatar.html')
