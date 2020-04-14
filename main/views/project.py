from .util import render, get_base_context, get_object_or_404, messages, JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import MusicTrackProject
from datetime import datetime


def get_project_or_404(request, id: int):
    '''
    Возвращает проект с нужным id + проверка на автора

    :param request: запрос клиента
    :param id: id проека в базе данных
    :rtype: MusicTrackProject
    '''

    project = get_object_or_404(MusicTrackProject, pk=id)
    if project.author != request.user:
        raise Http404

    return project


@login_required
def new_project(request):
    '''
    Страница создания проекта

    :param request: запрос клиента
    :return: страница создания проекта
    :rtype: HttpResponse
    '''

    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name', '')
        desc = request.POST.get('description', '')

        if not (0 < len(name) <= 50 and 0 <= len(desc) <= 250):
            return HttpResponseBadRequest('некорректные данные формы')

        exists = MusicTrackProject.objects.filter(
            author=request.user, name=name).exists()

        if exists:
            return HttpResponseBadRequest('проект с таким названием уже существует')

        proj_instance = MusicTrackProject.objects.create(
            name=name,
            desc=desc,
            author=request.user,
            creation_date=datetime.now()
        )

        messages.add_message(request, messages.SUCCESS,
                             'Проект успешно создан!')

        return JsonResponse({
            'proj_id': proj_instance.id
        })

    return render(request, 'project/new.html', get_base_context(request))


@login_required
def projects_list(request):
    '''
    Страница со списком проектов пользователя

    :param request: запрос клиента
    :return: список проектов
    :rtype: HttpResponse
    '''

    context = get_base_context(request)
    context['projects'] = MusicTrackProject.objects.filter(
        author=request.user).all()

    return render(request, 'project/list.html', context)


@login_required
def project_home(request, id: int):
    '''
    Главная страница проекта

    :param request: запрос клиента
    :param id: id проекта в базе данных
    :return: главная страница проекта
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, id)

    context = get_base_context(request)
    context['project'] = project

    return render(request, 'project/home.html', context)


def editor(request):
    '''
    Страница редактора мелодии

    :param request: запрос клиента
    :return: страница редактора мелодии
    :rtype: HttpResponse
    '''

    return render(request, 'project/pattern/editor.html', get_base_context(request))
