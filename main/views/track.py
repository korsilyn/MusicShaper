from .util import render, get_base_context, get_object_or_404, JsonResponse
from ..models import MusicTrack, TrackComment


def popular_tracks(request):
    '''
    Страница с популярными треками

    :param request: запрос клиента
    :return: Популярные треки
    :rtype: HttpResponse
    '''

    context = get_base_context(request)
    all_tracks = MusicTrack.objects.all()

    context["tracks"] = [{"name": tr.name, "id": tr.id, "likes": tr.likes, "desc": tr.desc,
                          "count": tr.listeners.count()} for tr in all_tracks]
    context["tracks"].sort(key=lambda i: i["count"], reverse=True)
    context["tracks"] = context["tracks"][:15]

    return render(request, 'track/popular.html', context)


def music_track_page(request, id):
    '''
    Страница просмотра (прослушивания) музыкального трека

    :param request: запрос клиента
    :param id: id трека
    :rtype: HttpResponse
    '''

    track = get_object_or_404(MusicTrack, pk=id)
    if request.is_ajax():
        track.comments.add(
            TrackComment.objects.create(author=request.user, topic=request.GET['topic'], content=request.GET['comment'],
                                        creation_date=datetime.now(), edit_date=datetime.now(),
                                        checked_by_author=True))
        track.save()
        return JsonResponse({"success": True})
    context = get_base_context(request)
    context['track'] = track
    return render(request, 'track/view.html', context)
