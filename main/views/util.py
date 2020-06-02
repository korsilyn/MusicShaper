'''
Вспомогательный модуль для view-модулей
'''

from django.http import Http404, JsonResponse


def get_base_context(request, update=None):
    '''
    Возвращает базовый контекст для всех страниц сайта

    :param request: запрос клиента
    :return: словарь контекста
    '''

    context = {
        'request': request,
        'user': request.user,
    }

    if isinstance(update, dict):
        context.update(update)

    return context


def ajax_view(method='POST', required_args=()):
    '''
    Декоратор для ajax-url'ов

    Итоговая view-функция автоматически проверяет
    `request.is_ajax()` и `request.method`
    '''

    if method not in ('GET', 'POST'):
        raise ValueError(f'invalid ajax_view method \'{method}\'''')

    def actual_decorator(view_func):

        def wrapper(request, *args, **kwargs):
            if not (request.is_ajax() and request.method == method):
                raise Http404

            q_dict = request.GET if method == 'GET' else request.POST
            print(q_dict)
            for r_arg in required_args:
                if r_arg not in q_dict:
                    raise Http404

            response = view_func(request, *args, **kwargs)
            return JsonResponse(response)

        return wrapper

    return actual_decorator
