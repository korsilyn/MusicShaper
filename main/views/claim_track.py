'''
Модуль жалоб на музыкальные треки
'''

from .util import get_base_context
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from ..models import MusicTrack, TrackComment
from ..forms import ClaimForm


@login_required
def claim_track(request: HttpRequest, track_id: int):
    context = get_base_context(request)
    track = get_object_or_404(MusicTrack, pk=track_id)

    if request.user == track.author:
        messages.add_message(request, messages.ERROR, "Вы не можете создать жалобу на свой трек!")
        return redirect('track', track_id=track_id)

    old_claim = track.claims.filter(author=request.user).first()
    context["old_claim"] = old_claim

    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            if old_claim:
                if (old_claim.content == form.data["content"]) and (old_claim.topic == form.data["topic"]):
                    messages.add_message(request, messages.ERROR, "Ничего не изменено")
                    return redirect('track', track_id=track_id)

                old_claim.topic = form.data["topic"]
                old_claim.content = form.data["content"]
                old_claim.save()
                messages.add_message(request, messages.SUCCESS, "Жалоба успешно отредактирована")
            else:
                new_claim = TrackComment.objects.create(
                    author=request.user,
                    topic=form.data["topic"],
                    content=form.data["content"],
                    creation_date=datetime.now(),
                    edit_date=datetime.now()
                )
                track.claims.add(new_claim)
                messages.add_message(request, messages.SUCCESS, "Жалоба успешно создана")

            return redirect('track', track_id=track_id)
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные формы")
            context["claimform"] = form
    else:
        context["claimform"] = ClaimForm(data={
            "topic": old_claim.topic if old_claim else "",
            "content": old_claim.content if old_claim else ""
        }
        )

    return render(request, 'track/claim_track.html', context)
