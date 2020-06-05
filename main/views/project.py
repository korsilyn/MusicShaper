'''
================================
Модуль view-функций для проектов
================================
'''

from itertools import zip_longest
from json import loads
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.messages import add_message, SUCCESS, ERROR
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import transaction
from .util import get_base_context, ajax_view
from ..models import MusicTrackProject, TrackPatternInstance
from ..forms import ProjectForm


def get_project_or_404(request, proj_id: int):
    '''
    **Возвращает проект с нужным id + проверка на автора**

    :param request: запрос клиента
    :param proj_id: id проека в базе данных
    :rtype: MusicTrackProject
    '''

    project = get_object_or_404(MusicTrackProject, pk=proj_id)
    if project.author != request.user:
        raise Http404

    return project


@login_required
def new_project(request):
    '''
    **Страница создания проекта**

    :param request: запрос клиента
    :return: страница создания проекта
    :rtype: HttpResponse
    '''

    if request.method == 'POST':
        form = ProjectForm(request.user, request.POST)
        if form.is_valid():
            project = form.save()
            add_message(request, SUCCESS, 'Проект успешно создан')
            return redirect('project_home', proj_id=project.id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = ProjectForm(request.user)

    context = get_base_context(request, {
        'form': form
    })

    return render(request, 'project/new.html', context)


@login_required
def projects_list(request):
    '''
    **Страница со списком проектов пользователя**

    :param request: запрос клиента
    :return: список проектов
    :rtype: HttpResponse
    '''

    context = get_base_context(request, {
        'projects': MusicTrackProject.objects.filter(author=request.user).all()
    })

    return render(request, 'project/list.html', context)


@login_required
def project_home(request, proj_id: int):
    '''
    **Главная страница проекта**

    :param request: запрос клиента
    :param proj_id: id проекта в базе данных
    :return: главная страница проекта
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, proj_id)

    return render(request, 'project/home.html', get_base_context(request, {
        'project': project,
        'timeline_edited': TrackPatternInstance.objects.filter(pattern__project=project).exists()
    }))


@login_required
def manage_project(request, proj_id: int):
    '''
    **Страница управления проектом**

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, proj_id)

    if request.method == 'POST':
        form = ProjectForm(request.user, instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Изменения успешно сохранены')
            return redirect('project_home', proj_id=proj_id)
        add_message(request, ERROR, 'Некорректные данные формы')
    else:
        form = ProjectForm(request.user, instance=project)

    context = get_base_context(request, {
        'project': project,
        'form': form,
    })

    return render(request, 'project/manage.html', context)


@login_required
def delete_project(request, proj_id: int):
    '''
    **Страница удаления проекта**

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, proj_id)

    if request.method == 'POST':
        project.delete()
        add_message(request, SUCCESS, 'Проект успешно удалён')
        return redirect('projects')

    context = get_base_context(request, {
        'title': 'Удаление проекта',
        'item_name': project.name,
        'confirm_title': 'Удалить проект',
        'cancel_title': 'Назад к настройкам',
        'cancel_url': reverse('manage_project', kwargs={
            'proj_id': project.pk
        })
    })

    return render(request, 'delete.html', context)


@login_required
def project_timeline(request, proj_id: int):
    '''
    Страница таймайна проекта

    :param request: запрос клиента
    :param proj_id: id проекта в БД
    :rtype: HttpResponse
    '''

    project = get_project_or_404(request, proj_id)

    if not project.patterns.exists():
        raise Http404

    patterns = {}
    instances = []
    for pat in project.patterns.all():
        patterns[pat.name] = pat.to_dict()
        instances += [i.to_dict() for i in pat.instances.all()]

    return render(request, 'timeline/editor.html', {
        'project': project,
        'instruments': {i.name: i.to_dict() for i in project.get_used_instruments()},
        'patterns': patterns,
        'instances': instances,
    })


def parse_json_pattern_instance(json):
    '''
    Вспомогательная функция. Возвращает словарь образца паттерна
    '''

    try:
        instance = loads(json)
    except (ValueError, TypeError):
        return None
    return {key: int(value) for key, value in instance.items()}


def handle_json_pattern_instance(json_instance, model_instance, proj_id):
    '''
    Вспомогательная функция. Обрабатывает модель образца
    паттерна по json данным из заспроса клиента
    '''

    instance = parse_json_pattern_instance(json_instance)
    if instance is None:
        if model_instance is not None and model_instance.pattern.project_id == proj_id:
            model_instance.delete()
    elif model_instance is None:
        model_instance = TrackPatternInstance(**instance)
        if model_instance.pattern.project_id == proj_id:
            model_instance.save()
    else:
        TrackPatternInstance.objects.filter(\
            id=model_instance.id, pattern__project__id=proj_id).update(**instance)


@login_required
@ajax_view(required_args=('bpm', 'instances[]'))
def save_timeline(request, proj_id: int):
    '''
    Ajax-функция для сохранения таймайна проекта
    '''

    project = get_project_or_404(request, proj_id)

    project.settings.bpm = request.POST['bpm']
    project.settings.save()

    instances_data = request.POST.getlist('instances[]', [])
    instances_models = TrackPatternInstance.objects.filter(pattern__project=project)

    if len(instances_data) == 1 and instances_data[0] == '':
        TrackPatternInstance.objects.filter(pattern__project=project).delete()
    else:
        with transaction.atomic():
            for json_i, model_i in zip_longest(instances_data, instances_models):
                handle_json_pattern_instance(json_i, model_i, proj_id)

    return {'success': True}
