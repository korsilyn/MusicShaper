from .util import render, redirect, get_base_context, get_object_or_404, JsonResponse
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required
from ..models import MusicTrackProject
from ..forms import CreateProjectForm
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

    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.creation_date = datetime.now()
            project.save()
            add_message(request, SUCCESS, 'Проект успешно создан')
            return redirect('project_home', id=project.id)
        else:
            add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = CreateProjectForm()

    context = get_base_context(request)
    context['form'] = form

    return render(request, 'project/new.html', context)


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
