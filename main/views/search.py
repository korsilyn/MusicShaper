'''
==============================
Модуль view-функций для поиска
==============================
'''

from difflib import SequenceMatcher
from operator import itemgetter
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import HttpResponseBadRequest, JsonResponse
from .util import get_base_context
from ..models import MusicTrack, user_to_dict


def similar(first, second):
    '''
    **Возвращает число, показывающее на сколько похожи последовательности first и second**

    :param first: первая последовательность
    :param second: второе последовательность
    :return: число от 0 до 1
    '''

    return SequenceMatcher(None, first, second).ratio()


def filter_similar(items, comp_value, threshold, key=None):
    '''
    **Фильтрует елементы списка последовательностей по схожести
    с другой последовательностью**
    Значение генератора - кортеж (элемент, схожесть)

    :param items: список последовательностей
    :param comp_value: последовательность для сравнения
    :param threshold: граница схожести от 0 до 1
    :param key: функция, возвращающая ключ сортировки елемента в списке
    :return: фильтрующий генератор
    '''

    if key is None:
        def key(item):
            return item

    for item in items:
        similarity = similar(key(item), comp_value)
        if similarity >= threshold:
            yield (item, similarity)


def filter_similar_sorted(*fs_args, reverse=False, **fs_kwargs):
    '''
    **Фильтрует елементы списка функцией filter_similar + сортирует
    результат по "схожестям"**

    :param fs_args: позиционные аргументы функции filter_similar
    :param fs_kwargs: проименованные аргументы функции filter_similar
    :param reverse: аналогичен аргументу reverse в функции sorted
    :return: фильтрующий генератор
    '''

    fs_generator = filter_similar(*fs_args, **fs_kwargs)
    return sorted(fs_generator, key=itemgetter(1), reverse=reverse)


def search_page(request):
    '''
    **Страница поиска пользователей / треков и т.п.**

    :param request: запрос клиента
    :return: страница поиска
    :rtype: HttpResponse
    '''

    if request.method == 'POST' and request.is_ajax():
        search_request = request.POST.get('request', None)
        results_type = request.POST.get('type', None)
        sort_by = request.POST.get('sortBy', None)

        if not (search_request and results_type and sort_by):
            raise HttpResponseBadRequest

        threshold = 0.6
        results = []

        if results_type == 'user':
            results = filter_similar_sorted(
                User.objects.all(), search_request, threshold,
                key=lambda u: u.username, reverse=True
            )
            results = list(map(lambda r: user_to_dict(r[0]), results))
        elif results_type == 'track':
            results = filter_similar(
                MusicTrack.objects.all(), search_request, threshold, lambda t: t.name
            )

            key_lambda = None
            if sort_by == 'relevant':
                key_lambda = lambda r: r[1]
            elif sort_by == 'popularity':
                key_lambda = lambda r: r[0].likes.count() + r[0].dislikes.count() # temp fix
            elif sort_by == 'likes':
                key_lambda = lambda r: r[0].likes.count()
            elif sort_by in ('new', 'old'):
                key_lambda = lambda r: r[0].creation_date
            else:
                raise HttpResponseBadRequest

            results = sorted(results, reverse=sort_by != 'old', key=key_lambda)
            results = list(map(lambda r: r[0].to_dict(), results))

        return JsonResponse({
            "results": results,
        })

    return render(request, 'search.html', get_base_context(request))
