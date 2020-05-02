from .util import render, redirect, get_base_context, get_object_or_404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from ..forms import CreateMusicInstrumentForm, SettingsModelForm
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
        form = CreateMusicInstrumentForm(request.POST)
        if form.is_valid():
            try:
                existed_i = MusicInstrument.objects.filter(
                    project=project, name=form.data['name']
                )
                if existed_i:
                    raise LookupError

                instrument = MusicInstrument.objects.create(
                    project=project,
                    name=form.data['name'],
                    type=form.data['type'],
                )
            except TypeError:
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
        form = CreateMusicInstrumentForm()

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
        'form': form
    })

    return render(request, 'instrument/edit.html', context)
