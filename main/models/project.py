from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .settings import ModelWithSettings, JSONSetting


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
    author = models.ForeignKey(User, models.CASCADE, 'projects')
    creation_date = models.DateTimeField()


class MusicInstrument(ModelWithSettings):
    '''
    Модель музыкального инстурмента

    :param name: имя инструмента в редакторе
    :param type: тип инструмента (из библиотеки Tone.js)
    :param project: проект
    '''

    name = models.CharField(max_length=25)
    type = models.CharField(max_length=10)
    project = models.ForeignKey(
        MusicTrackProject, models.CASCADE, 'instruments'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(MusicInstrumentSetting, 'instrument', *args, **kwargs)


class MusicInstrumentEffect(ModelWithSettings):
    '''
    Модель эффекта музыкального инструмента

    :param type: тип эффекта (из библиотеки Tone.js)
    :param instrument: инструмент
    '''

    type = models.CharField(max_length=25)
    instrument = models.ForeignKey(
        MusicInstrument, models.CASCADE, 'effects'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(MusicInstrumentEffectSetting, 'effect', *args, **kwargs)


class MusicInstrumentSetting(JSONSetting):
    '''
    Модель настройки музыкального инструмента

    :param instrument: инструмент
    '''

    instrument = models.ForeignKey(
        MusicInstrument, models.CASCADE, 'settings'
    )


class MusicInstrumentEffectSetting(JSONSetting):
    '''
    Модель настройки эффекта музыкального инструмента

    :param effect: эффект инструмента
    '''

    effect = models.ForeignKey(
        MusicInstrumentEffect, models.CASCADE, 'settings'
    )


class MusicTrackPattern(models.Model):
    '''
    Модель паттерна проекта

    :param name: имя паттерна
    :param color: цвет паттерна в редакторе
    :param duration: продолжительность
    '''

    project = models.ForeignKey(MusicTrackProject, models.CASCADE, 'patterns')
    name = models.CharField(max_length=25)
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

    pattern = models.ForeignKey(MusicTrackPattern, models.CASCADE, 'notes')
    position = models.FloatField(validators=[MinValueValidator(0)])
    duration = models.FloatField(validators=[MinValueValidator(0.05)])
    notation = models.PositiveIntegerField(choices=NOTATION_CHOICES)
    octave = models.PositiveIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(7)]
    )