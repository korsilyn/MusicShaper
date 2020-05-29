'''
Модуль вспомогательных фильтров django-шаблонов для строк
'''

from django import template


register = template.Library()


@register.filter(name='index')
def index_filter(arr, index):
    '''
    Возвращает элемент списка с индексом `index` (django-шаблоны)

    Если указанного элемента нет, возвращает `None`
    '''

    try:
        return arr[index]
    except IndexError:
        return None

@register.filter(name='range')
def range_filter(num):
    '''
    Аналог range(`num`)
    '''

    return range(num)
