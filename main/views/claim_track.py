'''
Модуль жалоб на музыкальные треки
'''

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required

from .util import get_base_context
from ..models import MusicTrack, TrackComment
from ..forms import ClaimForm


@login_required
def claim_track(request: HttpRequest, track_id: int):
    '''
    Страница создания / редактирования жалобы на трек

    :param request: запрос клиента
    :param track_id: id трека в БД
    :rtype: HttpResponse
    '''

    context = get_base_context(request)

    track = get_object_or_404(MusicTrack, pk=track_id)
    context['track'] = track

    if request.user == track.author:
        add_message(request, ERROR, 'Вы не можете создать жалобу на свой трек!')
        return redirect('track', track_id=track_id)

    old_claim = track.claims.filter(author=request.user).first()
    context['old_claim'] = old_claim

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            if old_claim:
                if old_claim.content == form.data['content']\
                and old_claim.topic == form.data['topic']:
                    add_message(request, ERROR, 'Ничего не изменено')
                    return redirect('track', track_id=track_id)

                old_claim.topic = form.data['topic']
                old_claim.content = form.data['content']
                old_claim.save()
                add_message(request, SUCCESS, 'Жалоба успешно отредактирована')
            else:
                new_claim = TrackComment.objects.create(
                    author=request.user,
                    topic=form.data['topic'],
                    content=form.data['content'],
                    creation_date=datetime.now(),
                    edit_date=datetime.now(),
                )
                track.claims.add(new_claim)
                add_message(request, SUCCESS, 'Жалоба успешно создана')
            return redirect('track', track_id=track_id)

        add_message(request, ERROR, 'Некорректные данные формы')
        context['claimform'] = form
    else:
        context['claimform'] = ClaimForm(data={
            'topic': old_claim.topic if old_claim else '',
            'content': old_claim.content if old_claim else ''
        })

    return render(request, 'track/claim_track.html', context)
