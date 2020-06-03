'''
Модуль view-функций для музыкальных треков
'''

from datetime import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required
from .util import get_base_context, ajax_view
from ..models import MusicTrack, TrackComment, TrackProjectSettings
from ..forms import MusicTrackForm
from .project import get_project_or_404

def popular_tracks(request):
    '''
    Страница с популярными треками

    :param request: запрос клиента
    :return: Популярные треки
    :rtype: HttpResponse
    '''

    all_tracks = MusicTrack.objects.all()
    context = get_base_context(request, {
        'tracks': sorted([{
            'name': tr.name, 'desc': tr.desc, 'id': tr.id,
            'likes': tr.likes, 'count': tr.listeners.count()
        } for tr in all_tracks], key=lambda i: i['count'], reverse=True)[:15]
    })

    return render(request, 'track/popular.html', context)


def track_view(request, track_id: int):
    '''
    Страница прослушивания музыкального трека

    :param request: запрос клиента
    :returns: страница трека
    '''

    track = get_object_or_404(MusicTrack, pk=track_id)

    if request.is_ajax():
        response = {'success': False}

        operation = request.GET['operation']
        if operation == 'send':
            track.comments.add(TrackComment.objects.create(
                author=request.user,
                topic=request.GET['topic'],
                content=request.GET['comment'],
                creation_date=datetime.now(),
                edit_date=datetime.now(),
            ))
            response['success'] = True
        elif operation == 'edit':
            c_id = request.GET['comment_id']
            comment = get_object_or_404(TrackComment, pk=c_id)
            comment.content = request.GET['comment']
            comment.save()
            response['success'] = True
        elif operation == 'delete':
            d_id = request.GET['comment_id']
            comment = get_object_or_404(TrackComment, pk=d_id)
            comment.delete()
            comment.save()
            response['success'] = True
        elif operation in ['like', 'dislike']:
            query = getattr(track, operation + 's', None)
            if query is not None:
                already = query.filter(pk=request.user.id).exists()
                if already:
                    query.remove(request.user)
                else:
                    query.add(request.user)
                response.update({
                    'success': True,
                    f'total_{operation}s': query.count()
                })

        if response['success']:
            track.save()
        return JsonResponse(response)

    context = get_base_context(request, {
        'track': track,
        'liked': track.likes.filter(pk=request.user.id).exists(),
        'disliked': track.dislikes.filter(pk=request.user.id).exists(),
        'total_likes': track.likes.count(),
        'total_dislikes': track.dislikes.count(),
    })

    return render(request, 'track/view.html', context)


@ajax_view
def upload_track(request, proj_id: int):
    '''
    Ajax-функция для загрузки аудио файла проекта.
    Возвращает клиенту url адрес формы публикации трека
    '''

    if 'audio' not in request.FILES:
        raise Http404

    project = get_project_or_404(request, proj_id)

    track = MusicTrack.objects.create(
        name=project.name,
        desc=project.desc,
        author=request.user,
        creation_date=datetime.now(),
        audio_file=request.FILES['audio'],
    )
    TrackProjectSettings.objects.create(
        track=track,
        access=0,
        allow_comments=True,
        allow_rating=True,
        allow_reusing=True,
    )

    return {'success': True}


def manage_track(request, track_id: int):
    '''
    Страница управления треком

    :param request: запрос клиента
    :param track_id: id трека в БД
    '''

    track = get_object_or_404(MusicTrack, id=track_id)
    if track.author != request.author:
        raise Http404

    if request.method == 'POST':
        form = MusicTrackForm(instance=track)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Изменения успешно сохранены')
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = MusicTrackForm()

    context = get_base_context(request, {
        'form': form,
        'track': track,
    })

    return render(request, 'track/manage.html', context)


@login_required
def delete_track(request, track_id: int):
    '''
    Страница удаления трека админом

    :param request: запрос клиента
    :param track_id: id трека в БД
    :rtype: HttpResponse
    '''

    track = get_object_or_404(MusicTrack, pk=track_id)

    if request.method == 'POST':
        track.delete()
        add_message(request, SUCCESS, 'Трек успешно удалён')
        return redirect('profile', username=track.author.username)

    context = get_base_context(request, {
        'title': 'Удаление трека',
        'item_name': track.name,
        'confirm_title': 'Удалить трек',
        'cancel_title': 'Назад к странице трека',
        'cancel_url': reverse('track', kwargs={
            'track_id': track.pk
        })
    })

    return render(request, 'delete.html', context)
