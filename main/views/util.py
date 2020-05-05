from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages


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
