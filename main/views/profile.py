'''
Модуль view-функций для профиля пользователя
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .util import get_base_context
from ..models import Profile, MusicTrack


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

    context = get_base_context(request, {
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
        add_message(request, SUCCESS, 'Профиль успешно обновлён')
        return redirect('profile')

    context = get_base_context(request, {
        'profile': profile
    })
    return render(request, 'profile/edit.html', context)


@login_required
def change_password(request):
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
            add_message(request, SUCCESS, 'Пароль успешно изменён')
            return redirect('profile')
        add_message(request, ERROR, 'Некорректные данные формы')
        return render(request, 'profile/change_password.html', {
            'form': form
        })

    context = get_base_context(request, {
        'form': PasswordChangeForm(user=request.user)
    })
    return render(request, 'profile/change_password.html', context)


@login_required
def delete_avatar(request):
    '''
    Страница удаления аватара

    :param request: запрос клиента
    :return: страница удаления аватара
    :rtype: HttpResponse
    '''

    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        profile.image.delete(save=True)
        add_message(request, SUCCESS, 'Аватар успешно удалён')
        return redirect('profile')

    return render(request, 'profile/delete_avatar.html')
