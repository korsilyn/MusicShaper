from .util import render, get_base_context, get_object_or_404, JsonResponse
from ..models import MusicTrack, TrackComment
from datetime import datetime


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
            'name': tr.name, 'id': tr.id, 'likes': tr.likes, 'desc': tr.desc, 'count': tr.listeners.count()
        } for tr in all_tracks], key=lambda i: i['count'], reverse=True)[:15]
    })

    return render(request, 'track/popular.html', context)


def track_view(request, id):
    '''
    Страница прослушивания музыкального трека

    :param request: запрос клиента
    :return: 
    '''

    track = get_object_or_404(MusicTrack, pk=id)

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
