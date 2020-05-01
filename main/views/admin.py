from .util import render, get_base_context, redirect
from ..forms import CreateTestTrack
from ..models import MusicTrack, TrackSettings
from datetime import datetime


def admins(request):
    return render(request, 'admin/admin.html', get_base_context(request))


def test_track(request):
    '''
    Страница создания пробного трека

    :param request: запрос клиента
    :return: страница создания пробного трека
    :rtype: HttpResponse
    '''
    is_test_track = request.method == 'POST'
    context = {
        "is_test_track": is_test_track,
        "is_valid": False,
        "form": CreateTestTrack(),
    }
    if is_test_track:
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
    return render(request, 'admin/test_track.html', context)
