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

    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name', '')
        if len(name) == 0 or len(name) > 25:
            return JsonResponse({
                'error': 'invalid name'
            })

        settings = dict()
        for key, value in request.POST.items():
            if key.startswith('settings_'):
                settings[key[9:]] = value
        
        instrument = MusicInstrument.objects.create(
            name=name,
            project=project
        )

        settings_file_content = ContentFile(json_dumps(settings))
        instrument.settings.save('i_' + name + '.json', settings_file_content)
        instrument.save()
        
        return JsonResponse({
            'success': True
        })

    context = get_base_context(request)
    context['project'] = project

    return render(request, 'project/instrument/new.html', context)
