'''
Модуль Django-admin

В нём нужно регистрировать модели из базы данных,
чтобы они были видны на странице `admin:index`
'''

from django.contrib import admin
from .models import Profile, MusicTrack

admin.site.register(Profile)
admin.site.register(MusicTrack)
