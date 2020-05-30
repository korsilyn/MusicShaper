'''
Модуль вспомогательных фильтров django-шаблонов для строк
'''

from django import template


register = template.Library()


@register.filter(name='split')
def split_filter(string, sep):
    '''
    Аналог функции str.split для django-шаблонов
    '''

    return string.split(sep)
