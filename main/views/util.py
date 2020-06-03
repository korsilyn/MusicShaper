'''
=======================================
Вспомогательный модуль для view-модулей
=======================================
'''


def get_base_context(request, update=None):
    '''
    **Возвращает базовый контекст для всех страниц сайта**

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
