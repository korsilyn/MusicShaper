'''
Модуль view-функций для паттернов
'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.http import JsonResponse
from ..models import MusicTrackPattern
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

    if request.method == 'GET' and request.is_ajax():
        operation = request.GET.get('operation', None)
        response = {'success': False}

        if operation == 'loadInstrument':
            name = request.GET.get('instrumentName', '')
            instr = project.instruments.filter(name=name).first()
            if instr is not None:
                response.update({
                    'success': True,
                    name: instr.get_settings()
                })

        return JsonResponse(response)

    context = get_base_context(request, {
        'project': project,
        'pattern': pattern,
        'usedInstruments': {},
        'allInstruments': list(project.instruments\
            .values_list('name', flat=True))
    })

    for instrument in pattern.get_instruments():
        context['usedInstruments'][instrument.name] = instrument.get_settings()

    return render(request, 'pattern/editor.html', context)
