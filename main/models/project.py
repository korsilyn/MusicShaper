from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


class MusicTrackProject(models.Model):
    '''
    Модель проекта

    :param name: имя проекта
    :param desc: описание
    :param author: автор
    :param patterns: список паттернов
    :param data: файл с данными проекта (настройки, инструменты и т.д.)
    '''

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, models.CASCADE, "projects")
    creation_date = models.DateTimeField()


class MusicInstrument(models.Model):
    '''
    Абстрактная модель музыкального инстурмента

    Неабстрактный класс модели должен реализовывать
    метод get_type, возвращающий тип инструмента
    из библиотеки Tone.js

    :param name: имя инструмента в редакторе
    :param project: проект
    '''

    class Meta:
        abstract = True

    name = models.CharField(max_length=25)
    project = models.ForeignKey(
        MusicTrackProject, models.CASCADE, "instruments"
    )

    def get_type(self) -> str:
        raise NotImplementedError


class MusicInstrumentEffect(models.Model):
    '''
    Абстрактная модель эффекта музыкального инструмента
    (эхо, искажение и т.д.)

    :param instrument: музыкальный инструмент
    '''

    class Meta:
        abstract = True

    instrument = models.ForeignKey(MusicInstrument, models.CASCADE, "effects")

    def get_type(self) -> str:
        raise NotImplementedError


@register.filter
@stringfilter
def get_type(obj):
    if obj is MusicInstrument or obj is MusicInstrumentEffect:
        return obj.get_type()


class MusicTrackPattern(models.Model):
    '''
    Модель паттерна проекта

    :param name: имя паттерна
    :param color: цвет паттерна в редакторе
    :param duration: продолжительность
    '''

    name = models.CharField(max_length=25)
    project = models.ForeignKey(MusicTrackProject, models.CASCADE, "patterns")
    color = models.CharField(max_length=25)
    duration = models.FloatField()


class MusicNote(models.Model):
    '''
    Модель музыкальной ноты в паттерне

    :param pattern: паттерн
    :param position: момент времени, в который должна играть нота
    :param duration: длительность ноты
    :param notation: буквенная нотация ноты
    :param octave: октава
    '''

    NOTATION_CHOICES = [
        (1,  'C'),  (2, 'C#'),
        (3,  'D'),  (4, 'D#'),
        (5,  'E'),
        (6,  'F'),  (7,  'F#'),
        (8,  'G'),  (9,  'G#'),
        (10, 'A'),  (11, 'A#'),
        (12, 'B'),
    ]

    pattern = models.ForeignKey(MusicTrackPattern, models.CASCADE, "notes")
    position = models.FloatField(validators=[MinValueValidator(0)])
    duration = models.FloatField(validators=[MinValueValidator(0.05)])
    notation = models.PositiveIntegerField(choices=NOTATION_CHOICES)
    octave = models.PositiveIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(7)]
    )

