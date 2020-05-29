'''
Модуль view-функций для вкладки `Администрация`
'''

from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import user_passes_test, login_required
from .util import get_base_context
from ..forms import CreateTestTrack
from ..models import MusicTrack, TrackSettings


superuser_check = lambda u: u.is_superuser


@login_required
@user_passes_test(superuser_check)
def admin_home(request):
    '''
    Панель администрации

    :param request: запрос клиента
    :rtype: HttpResponse
    '''

    return render(request, 'admin/admin.html', get_base_context(request))


@login_required
@user_passes_test(superuser_check)
def create_test_track(request):
    '''
    Страница создания пробного трека

    :param request: запрос клиента
    :return: страница создания пробного трека
    :rtype: HttpResponse
    '''

    if request.method == 'POST':
        form = CreateTestTrack(request.POST)
        if form.is_valid():
            name = form.data['name']
            desc = form.data['desc']
            allow_rating = form.data.get('allow_rating', 'off') == 'on'
            allow_reusing = form.data.get('allow_reusing', 'off') == 'on'
            allow_comments = form.data.get('allow_comments', 'off') == 'on'
            track = MusicTrack.objects.create(
                name=name, desc=desc,
                author=request.user,
                creation_date=datetime.now(),
            )
            TrackSettings.objects.create(
                track=track,
                allow_rating=allow_rating,
                allow_reusing=allow_reusing,
                allow_comments=allow_comments,
            )
            add_message(request, SUCCESS, 'Трек успешно создан')
            return redirect('track', track_id=track.id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = CreateTestTrack()

    context = get_base_context(request, {
        'form': form
    })

    return render(request, 'admin/create_test_track.html', context)


@login_required
@user_passes_test(superuser_check)
def claimed_track(request):
    context = get_base_context(request)

    all_tracks = MusicTrack.objects.all()
    context["tracks"] = [{"name": t.name, "id": t.id, "count": t.get_claims_count()}
                         for t in all_tracks]
    context["tracks"].sort(key=lambda i: i["count"], reverse=True)
    context["tracks"] = filter(lambda t: t["count"] > 0, context["tracks"])

    return render(request, 'admin/claimed_track.html', context)
