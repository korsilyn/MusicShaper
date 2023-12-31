'''
=================================
Модуль view-функций для паттернов
=================================
'''

from itertools import zip_longest
from json import loads
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.http import Http404
from django.forms.models import model_to_dict
from django.urls import reverse
from django.db import transaction
from ..models import MusicTrackPattern, MusicNote
from ..forms import TrackPatternForm
from .project import get_project_or_404
from .util import get_base_context, ajax_view


@login_required
def patterns_list(request, proj_id: int):
    '''
    **Страница со списком паттернов в проекте**

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    '''

    project = get_project_or_404(request, proj_id)

    if not project.instruments.exists():
        raise Http404

    context = get_base_context(request, {
        'project': project,
        'patterns': MusicTrackPattern.objects.filter(project=project).all()
    })

    return render(request, 'pattern/list.html', context)


@login_required
def new_pattern(request, proj_id: int):
    '''
    **Страница создания паттерна**

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    '''

    project = get_project_or_404(request, proj_id)

    if not project.instruments.exists():
        raise Http404

    if request.method == 'POST':
        form = TrackPatternForm(project, data=request.POST)
        if form.is_valid():
            p_id = form.save().pk
            add_message(request, SUCCESS, 'Паттерн успешно создан')
            return redirect('pattern_editor', proj_id=proj_id, pat_id=p_id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = TrackPatternForm(project)

    context = get_base_context(request, {
        'project': project,
        'form': form
    })

    return render(request, 'pattern/new.html', context)


def parse_json_note(json):
    '''
    **Вспомогательная функция. Возвращает словарь
    музыкальной ноты из json строки**
    '''

    try:
        note = loads(json)
    except (ValueError, TypeError):
        return None
    note = {key: int(value) for key, value in note.items()}
    note['instrument_id'] = note.pop('instrument')
    return note


def handle_json_note(json_note, model_note, pat_id):
    '''
    **Вспомогательная функция. Обрабатывает модель
    ноты по json данным из запроса клиента**
    '''

    note = parse_json_note(json_note)
    if note is None:
        if model_note is not None and model_note.pattern_id == pat_id:
            model_note.delete()
    elif model_note is None:
        MusicNote.objects.create(pattern_id=pat_id, **note)
    else:
        MusicNote.objects.filter(id=model_note.id, pattern__id=pat_id).update(**note)


@login_required
def pattern_editor(request, proj_id: int, pat_id: int):
    '''
    **Редактор паттерна**

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param pat_id: id паттерна в БД
    '''

    project = get_project_or_404(request, proj_id)
    pattern = get_object_or_404(MusicTrackPattern, pk=pat_id, project=project)

    if project.instruments.count() == 0:
        add_message(request, ERROR, 'В вашем проекте ещё нет музыкальных инструментов!')
        return redirect('instruments', proj_id=proj_id)

    instruments = list(pattern.get_instruments())
    music_notes = MusicNote.objects.filter(pattern=pattern)

    return render(request, 'pattern/editor.html', {
        'project': project,
        'pattern': pattern,
        'usedInstruments': {i.name: i.to_dict() for i in instruments},
        'allInstruments': list(project.instruments.values_list('name', flat=True)),
        'musicNotes': list(map(model_to_dict, music_notes)),
    })


@login_required
@ajax_view(required_args=('notes[]', 'bpm'))
def save_pattern(request, proj_id: int, pat_id: int):
    '''
    Сохраняет паттерн по ajax POST запросу
    '''

    project = get_project_or_404(request, proj_id)

    project.settings.bpm = request.POST['bpm']
    project.settings.save()

    pattern = get_object_or_404(MusicTrackPattern, pk=pat_id, project=project)

    music_notes = MusicNote.objects.filter(pattern=pattern)
    notes = request.POST.getlist('notes[]', [])

    if len(notes) == 1 and notes[0] == '':
        MusicNote.objects.filter(pattern=pattern).delete()
    else:
        with transaction.atomic():
            for json_note, model_note in zip_longest(notes, music_notes):
                handle_json_note(json_note, model_note, pat_id)

    return {'success': True}


@login_required
def manage_pattern(request, proj_id: int, pat_id: int):
    '''
    **Страница управления паттерном**

    :param request: запрос пользователя
    :param proj_id: id проекта в БД
    :param pat_id: id паттерна в БД
    '''

    project = get_project_or_404(request, proj_id)
    pattern = get_object_or_404(MusicTrackPattern, pk=pat_id)

    if request.method == 'POST':
        form = TrackPatternForm(project, instance=pattern, data=request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Изменения успешно сохранены')
            return redirect('manage_pattern', proj_id=proj_id, pat_id=pat_id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = TrackPatternForm(project, instance=pattern)

    context = get_base_context(request, {
        'project': project,
        'pattern': pattern,
        'form': form,
    })

    return render(request, 'pattern/manage.html', context)


@login_required
def delete_pattern(request, proj_id: int, pat_id: int):
    '''
    **Страница удаления паттерна**

    :param request: запрос пользователя
    :param proj_id: id проекта в БД
    :param pat_id: id паттерна в БД
    '''

    project = get_project_or_404(request, proj_id)
    pattern = get_object_or_404(MusicTrackPattern, pk=pat_id)

    if request.method == 'POST':
        pattern.delete()
        add_message(request, SUCCESS, 'Паттерн успешно удалён')
        return redirect('patterns', proj_id=proj_id)

    context = get_base_context(request, {
        'project': project,
        'title': 'Удаление паттерна',
        'item_name': pattern.name,
        'confirm_title': 'Удалить паттерн',
        'cancel_title': 'Назад к паттерну',
        'cancel_url': reverse('manage_pattern', kwargs={
            'proj_id': project.pk,
            'pat_id': pattern.pk
        })
    })

    return render(request, 'delete.html', context)
