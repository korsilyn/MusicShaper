from .util import render, redirect, get_base_context, get_object_or_404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from ..forms import MusicInstrumentForm, SettingsModelForm
from .project import get_project_or_404
from ..models import MusicInstrument


@login_required
def instruments(request, id: int):
    '''
    Страница со списком всех музыкальных инструментов
    в проекте

    :param request: запрос клиента
    :param id: id проекта в базе данных
    :return: список инструментов
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, id)

    context = get_base_context(request, {
        'project': project,
        'instruments': project.instruments
    })

    return render(request, 'instrument/list.html', context)


@login_required
def new_instrument(request, id: int):
    '''
    Страница создания музыкального инструмента

    :param request: запрос клиента
    :param id: id проекта в базе данных
    :return: страница создания инструмента
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, id)

    if request.method == 'POST':
        form = MusicInstrumentForm(request.POST)
        if form.is_valid():
            try:
                existed_i = MusicInstrument.objects.filter(
                    project=project, name=form.data['name']
                )
                if existed_i:
                    raise LookupError

                instrument = form.instance
                instrument.project = project
                instrument.save()
            except TypeError as err:
                add_message(request, ERROR, 'Неизвестный тип инструмента')
            except LookupError:
                add_message(
                    request, ERROR, 'Инструмент с таким именем уже существует'
                )
            else:
                add_message(request, SUCCESS, 'Инструмент успешно создан')
                return redirect('edit_instrument', proj_id=id, id=instrument.id)
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = MusicInstrumentForm()

    context = get_base_context(request, {
        'project': project,
        'form': form
    })

    return render(request, 'instrument/new.html', context)


@login_required
def edit_instrument(request, proj_id: int, id: int):
    '''
    Страница редактирования настроек инструмента

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param id: id инстуремнта в БД
    '''

    project = get_project_or_404(request, proj_id)
    instrument = get_object_or_404(MusicInstrument, pk=id)

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
def manage_instrument(request, proj_id: int, id: int):
    '''
    Страница управления инструментом

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param id: id инстуремнта в БД
    '''

    project = get_project_or_404(request, proj_id)
    instrument = get_object_or_404(MusicInstrument, pk=id)

    if request.method == 'POST':
        form = MusicInstrumentForm(instance=instrument, data=request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Изменения успешно сохранены')
            return redirect('edit_instrument', proj_id=proj_id, id=id)
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = MusicInstrumentForm(instance=instrument)

    context = get_base_context(request, {
        'project': project,
        'instrument': instrument,
        'form': form,
    })

    return render(request, 'instrument/manage.html', context)


@login_required
def delete_instrument(request, proj_id: int, id: int):
    '''
    Страница удаления инструмента

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :param id: id инстуремнта в БД
    '''

    project = get_project_or_404(request, proj_id)
    instrument = get_object_or_404(MusicInstrument, pk=id)

    if request.method == 'POST':
        instrument.delete()
        add_message(request, SUCCESS, 'Инструмент успешно удалён')
        return redirect('instruments', id=proj_id)

    context = get_base_context(request, {
        'project': project,
        'instrument': instrument,
    })

    return render(request, 'instrument/delete.html', context)
