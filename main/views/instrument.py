from .util import render, get_base_context, JsonResponse
from django.contrib.auth.decorators import login_required
from .project import get_project_or_404


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

    context = get_base_context(request)
    context['project'] = project

    return render(request, 'project/instrument/new.html', context)
