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

    context = get_base_context(request)
    all_tracks = MusicTrack.objects.all()

    context["tracks"] = [{"name": tr.name, "id": tr.id, "likes": tr.likes, "desc": tr.desc,
                          "count": tr.listeners.count()} for tr in all_tracks]
    context["tracks"].sort(key=lambda i: i["count"], reverse=True)
    context["tracks"] = context["tracks"][:15]

    return render(request, 'track/popular.html', context)


def music_track_page(request, id):
    track = get_object_or_404(MusicTrack, pk=id)
    if request.is_ajax():
        if request.GET['operation'] == "send":
            track.comments.add(
                TrackComment.objects.create(author=request.user, topic=request.GET['topic'],
                                            content=request.GET['comment'],
                                            creation_date=datetime.now(), edit_date=datetime.now(),
                                            checked_by_author=True))
            track.save()
            return JsonResponse({"success": True})
        elif request.GET['operation'] == "edit":
            comment_id = request.GET['comment_id']
            comment = get_object_or_404(TrackComment, pk=comment_id)
            comment.content = request.GET['comment']
            comment.save()
            return JsonResponse({"success": True})
        elif request.GET['operation'] == 'like':
            liked = track.likes.filter(pk=request.user.id).count() != 0
            if liked:
                track.likes.remove(request.user)
            else:
                track.likes.add(request.user)
            track.save()
            return JsonResponse({"success": True, "total_likes": track.likes.count()})
        elif request.GET['operation'] == 'dislike':
            disliked = track.dislikes.filter(pk=request.user.id).count() != 0
            if disliked:
                track.dislikes.remove(request.user)
            else:
                track.dislikes.add(request.user)
            track.save()
            return JsonResponse({"success": True, "total_dislikes": track.dislikes.count()})
        return JsonResponse({"success": False})
    context = get_base_context(request)
    context['track'] = track
    context['liked'] = track.likes.filter(pk=request.user.id).count() != 0
    context['disliked'] = track.dislikes.filter(pk=request.user.id).count() != 0
    context['total_likes'] = track.likes.count()
    context['total_dislikes'] = track.dislikes.count()
    return render(request, 'track/view.html', context)
