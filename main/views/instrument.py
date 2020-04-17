from .util import render, redirect, get_base_context, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import add_message, SUCCESS, ERROR
from ..forms import CreateMusicInstrumentForm
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

    context = get_base_context(request)
    context['project'] = project
    context['instruments'] = project.instruments

    return render(request, 'project/instrument/list.html', context)


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

                i = MusicInstrument.objects.create(
                    project=project,
                    name=form.data['name'],
                    type=form.data['type'],
                )
                i.set_default_settings()
            except NameError:
                add_message(request, ERROR, 'Неизвестный тип инструмента')
            except LookupError:
                add_message(
                    request, ERROR, 'Инструмент с таким именем уже существует'
                )
            else:
                add_message(request, SUCCESS, 'Инструмент успешно создан')
                return redirect('instruments', id=id)
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = CreateMusicInstrumentForm()

    context = get_base_context(request)
    context['project'] = project
    context['form'] = form

    return render(request, 'project/instrument/new.html', context)
