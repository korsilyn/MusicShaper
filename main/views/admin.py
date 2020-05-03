from .util import render, get_base_context, redirect
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import user_passes_test, login_required
from ..forms import CreateTestTrack
from ..models import MusicTrack, TrackSettings
from datetime import datetime


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
            return redirect('track', id=track.id)
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = CreateTestTrack()

    context = get_base_context(request, {
        'form': form
    })

    return render(request, 'admin/create_test_track.html', context)
