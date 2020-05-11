'''
Модуль view-функций для музыкальных инструментов
'''

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from .util import get_base_context
from ..forms import MusicInstrumentForm, SettingsModelForm
from .project import get_project_or_404
from ..models import MusicInstrument


@login_required
def instruments(request, proj_id: int):
    '''
    Страница со списком всех музыкальных инструментов
    в проекте

    :param request: запрос клиента
    :param proj_id: id проекта в базе данных
    :return: список инструментов
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, proj_id)

    context = get_base_context(request, {
        'project': project,
        'instruments': project.instruments
    })

    return render(request, 'instrument/list.html', context)


@login_required
def new_instrument(request, proj_id: int):
    '''
    Страница создания музыкального инструмента

    :param request: запрос клиента
    :param proj_id: id проекта в базе данных
    :return: страница создания инструмента
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, proj_id)

    if request.method == 'POST':
        form = MusicInstrumentForm(project, data=request.POST)
        if form.is_valid():
            try:
                existed_i = MusicInstrument.objects.filter(
                    project=project, name=form.data['name']
                )
                if existed_i:
                    raise LookupError

                instrument = form.save()
            except TypeError:
                add_message(request, ERROR, 'Неизвестный тип инструмента')
            except LookupError:
                add_message(
                    request, ERROR, 'Инструмент с таким именем уже существует'
                )
            else:
                add_message(request, SUCCESS, 'Инструмент успешно создан')
                return redirect('edit_instrument', proj_id=proj_id, instr_id=instrument.id)
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = MusicInstrumentForm(project)

    context = get_base_context(request, {
        'project': project,
        'form': form
    })

    return render(request, 'instrument/new.html', context)


@login_required
def edit_instrument(request, proj_id: int, instr_id: int):
    '''
    Страница редактирования настроек инструмента

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param instr_id: id инстуремнта в БД
    '''

    project = get_project_or_404(request, proj_id)
    instrument = get_object_or_404(MusicInstrument, pk=instr_id)

    if request.method == 'POST':
        form = SettingsModelForm(instance=instrument, data=request.POST)
        if form.is_valid():
            instrument = form.save()
            add_message(request, SUCCESS, 'Изменения успешно сохранены')
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = SettingsModelForm(instance=instrument)

    context = get_base_context(request, {
        'project': project,
        'instrument': instrument,
        'form': form,
    })

    return render(request, 'instrument/edit.html', context)


@login_required
def manage_instrument(request, proj_id: int, instr_id: int):
    '''
    Страница управления инструментом

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param instr_id: id инстуремнта в БД
    '''

    project = get_project_or_404(request, proj_id)
    instrument = get_object_or_404(MusicInstrument, pk=instr_id)

    if request.method == 'POST':
        form = MusicInstrumentForm(project, instance=instrument, data=request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Изменения успешно сохранены')
            return redirect('edit_instrument', proj_id=proj_id, instr_id=instr_id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = MusicInstrumentForm(project, instance=instrument)

    context = get_base_context(request, {
        'project': project,
        'instrument': instrument,
        'form': form,
    })

    return render(request, 'instrument/manage.html', context)


@login_required
def delete_instrument(request, proj_id: int, instr_id: int):
    '''
    Страница удаления инструмента

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param instr_id: id инстуремнта в БД
    '''

    project = get_project_or_404(request, proj_id)
    instrument = get_object_or_404(MusicInstrument, pk=instr_id)

    if request.method == 'POST':
        instrument.delete()
        add_message(request, SUCCESS, 'Инструмент успешно удалён')
        return redirect('instruments', proj_id=proj_id)

    context = get_base_context(request, {
        'project': project,
        'title': 'Удаление инструмента',
        'item_name': instrument.name,
        'confirm_title': 'Удалить инструмент',
        'cancel_title': 'Назад к настройкам',
        'cancel_url': reverse('manage_instrument', kwargs={
            'proj_id': project.pk,
            'instr_id': instrument.pk
        })
    })

    return render(request, 'delete.html', context)
