'''
============================================
Модуль view-функций для профиля пользователя
============================================
'''

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import Http404
from PIL import Image
from .util import get_base_context
from ..models import Profile, MusicTrack

def profile_page(request, username):
    '''
    **Страница профиля**

    :param request: запрос клиента
    :return: страница профиля
    :rtype: HttpResponse
    '''

    view_my_profile = not isinstance(username, str)
    user = request.user if view_my_profile else get_object_or_404(User, username=username)

    if view_my_profile and request.user.is_anonymous:
        raise Http404

    context = get_base_context(request, {
        "profile": user.profile,
        "tracks": MusicTrack.objects.filter(author=user),
        "likes": MusicTrack.objects.filter(likes=user),
    })

    if not view_my_profile and not request.user.is_anonymous:
        is_sub = user.profile.subscribers.filter(pk=request.user.profile.pk).exists()
        context['is_sub'] = is_sub

    return render(request, 'profile/view.html', context)


@login_required
def profile_edit_page(request):
    '''
    **Страница редактирования профиля**

    :param request: запрос клиента
    :return: страница редактирования профиля
    :rtype: HttpResponse
    '''

    profile = request.user.profile

    if request.method == 'POST':
        status = request.POST.get('status', '')
        image = request.FILES.get('image', None)
        if len(status) <= 100:
            profile.status = status
            add_message(request, SUCCESS, 'Статус успешно обновлён')
        else:
            add_message(request, ERROR, 'Максимальная длина статуса: 100 символов')
        if image:
            pil_image = Image.open(image)
            if pil_image.height <= 200 or pil_image.width <= 200:
                add_message(request, ERROR, 'Минимальное разрешение аватара: 200x200px')
            elif pil_image.height >= 800 or pil_image.width >= 800:
                add_message(request, ERROR, 'Максимальное разрешение аватара: 800x800px')
            elif image.size >= 4194304:
                add_message(request, ERROR, 'Максимальный размер аватарки: 4МБайта')
            else:
                profile.image.delete(save=True)
                profile.image = image
                add_message(request, SUCCESS, 'Аватар успешно обновлён')
            pil_image.close()
        profile.save()
        return redirect('profile')

    context = get_base_context(request, {
        'profile': profile
    })
    return render(request, 'profile/edit.html', context)


@login_required
def change_password(request):
    '''
    **Страница смены пароля**

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
    **Страница удаления аватара**

    :param request: запрос клиента
    :return: страница удаления аватара
    :rtype: HttpResponse
    '''

    profile = request.user.profile

    if request.method == 'POST':
        profile.image.delete(save=True)
        add_message(request, SUCCESS, 'Аватар успешно удалён')
        return redirect('profile')

    context = get_base_context(request, {
        'title': 'Удаление аватара',
        'confirm_title': 'Удалить аватар',
        'cancel_title': 'Назад к настройкам',
        'cancel_url': reverse('profile_edit'),
    })

    return render(request, 'delete.html', context)


@login_required
def subscribe(request, username):
    '''
    **Функция для добавления пользователя в подписки**

    :param request: запрос клиента
    :param username: юзернейм другого пользователя
    '''

    subscriber = request.user.profile
    target = get_object_or_404(Profile, user__username=username)

    already_sub = target.subscribers.filter(pk=subscriber.pk).exists()
    if target == subscriber or already_sub:
        add_message(request, ERROR, 'Недопустимая операция')
        return redirect('profile', username=username)

    target.subscribers.add(subscriber)
    target.save()

    add_message(request, SUCCESS, f'{username} был добавлен в ваши подписки')
    return redirect('profile', username=username)


@login_required
def unsubscribe(request, username):
    '''
    **Функция для удаления пользователя из подпискок**

    :param request: запрос клиента
    :param username: юзернейм другого пользователя
    '''

    subscriber = request.user.profile
    target = get_object_or_404(Profile, user__username=username)

    not_sub = not target.subscribers.filter(pk=subscriber.pk).exists()
    if target == subscriber or not_sub:
        add_message(request, ERROR, 'Недопустимая операция')
        return redirect('profile', username=username)

    target.subscribers.remove(subscriber)
    target.save()

    add_message(request, SUCCESS, f'{username} был удалён из ваших подписок')
    return redirect('profile', username=username)


@login_required
def subscriptions_page(request):
    '''
    **Функция для отображения полного списка подписок**

    :param request: запрос клиента
    :rtype: HttpResponse
    '''

    user = request.user
    context = get_base_context(request, {'profile': user.profile})
    is_sub = user.profile.subscribers.filter(pk=request.user.profile.pk).exists()
    context['is_sub'] = is_sub
    return render(request, 'profile/subscriptions.html', context)
