'''
Модуль view-функций для паттернов
'''

from itertools import zip_longest
from json import loads
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.http import JsonResponse
from django.forms.models import model_to_dict
from ..models import MusicTrackPattern, MusicNote, MusicInstrument
from ..forms import MusicPatternForm
from .project import get_project_or_404
from .util import get_base_context


@login_required
def patterns_list(request, proj_id: int):
    '''
    Страница со списком паттернов в проекте

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    '''

    project = get_project_or_404(request, proj_id)
    context = get_base_context(request, {
        'project': project,
        'patterns': MusicTrackPattern.objects.filter(project=project).all()
    })

    return render(request, 'pattern/list.html', context)


@login_required
def new_pattern(request, proj_id: int):
    '''
    Страница создания паттерна

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    '''

    project = get_project_or_404(request, proj_id)

    if request.method == 'POST':
        form = MusicPatternForm(project, data=request.POST)
        if form.is_valid():
            p_id = form.save().pk
            add_message(request, SUCCESS, 'Паттерн успешно создан')
            return redirect('pattern_editor', proj_id=proj_id, pat_id=p_id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = MusicPatternForm(project)

    context = get_base_context(request, {
        'project': project,
        'form': form
    })

    return render(request, 'pattern/new.html', context)


def make_instrument_dict(instruments):
    '''
    Вспомогательная функция. Возвращает словарь
    музыкальных инструментов (генератор)
    '''

    for instr in instruments:
        yield instr.name, instr.to_dict()


def parse_json_note(json, instruments):
    '''
    Вспомогательная функция. Возвращает словарь
    музыкальной ноты из json строки
    '''

    try:
        note = loads(json)
    except (ValueError, TypeError):
        return None
    note = {key: int(value) for key, value in note.items()}
    instr_id = note['instrument']
    note['instrument'] = next((i for i in instruments if i.id == instr_id), None)
    if note['instrument'] is None:
        note['instrument'] = MusicInstrument.objects.get(pk=instr_id)
        instruments.append(note['instrument'])
    return note


def handle_json_note(json_note, model_note, pattern, instruments):
    '''
    Вспомогательная функция. Обрабатывает модель
    ноты по json данным из запроса клиента
    '''

    note = parse_json_note(json_note, instruments)
    if note is None:
        model_note.delete()
    elif model_note is None:
        MusicNote.objects.create(pattern=pattern, **note)
    else:
        for key, value in note.items():
            setattr(model_note, key, value)
        model_note.save()


@login_required
def pattern_editor(request, proj_id: int, pat_id: int):
    '''
    Редактор паттерна

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

    if request.is_ajax():
        response = {'success': False}

        if request.method == 'GET':
            operation = request.GET.get('operation', None)

            if operation == 'loadInstrument':
                name = request.GET.get('instrumentName', '')
                instr = project.instruments.filter(name=name).first()
                if instr is not None:
                    response.update({
                        instr.name: instr.to_dict(),
                        'success': True
                    })

        elif request.method == 'POST':
            operation = request.POST.get('operation', None)

            if operation == 'save':
                notes = request.POST.getlist('notes[]', [])
                response['success'] = True
                model_notes = MusicNote.objects.filter(pattern=pattern)
                for json_note, model_note in zip_longest(notes, model_notes):
                    handle_json_note(json_note, model_note, pattern, instruments)

        return JsonResponse(response)

    return render(request, 'pattern/editor.html', {
        'project': project,
        'pattern': pattern,
        'usedInstruments': dict(make_instrument_dict(instruments)),
        'allInstruments': list(project.instruments.values_list('name', flat=True)),
        'musicNotes': list(map(model_to_dict, MusicNote.objects.filter(pattern=pattern))),
    })
