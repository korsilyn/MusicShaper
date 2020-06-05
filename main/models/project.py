'''
===========================
Модуль моделей для проектов
===========================
'''

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .settings import ModelWithSettings, FloatSettingValue


COLOR_CHOICES = [
    ('#ff0000', 'red'),
    ('#00ff00', 'green'),
    ('#0000ff', 'blue'),
    ('#00ffff', 'aqua'),
    ('#ff69b4', 'pink'),
    ('#cc33ff', 'purple'),
    ('#ff6600', 'orange'),
]


class MusicTrackProject(models.Model):
    '''
    **Модель проекта**

    :param name: имя проекта
    :param desc: описание
    :param author: автор
    :param creation_date: дата создания
    '''

    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=250)
    author = models.ForeignKey(User, models.CASCADE, 'projects')
    creation_date = models.DateTimeField()

    def get_used_instruments(self):
        '''
        Возвращает список инструментов, использующихся
        в паттернах проекта
        '''

        return MusicInstrument.objects.filter(project=self, notes__isnull=False)


class TrackProjectSettings(models.Model):
    '''
    **Модель настроек проекта**

    :param project: проект
    :param bpm: темп итогового трека
    '''

    project = models.OneToOneField(MusicTrackProject, models.CASCADE, related_name='settings')
    bpm = models.PositiveIntegerField(validators=[
        MinValueValidator(32),
        MaxValueValidator(999),
    ])


class MusicInstrument(ModelWithSettings):
    '''
    **Модель музыкального инстурмента**

    :param name: имя инструмента в редакторе
    :param project: проект
    '''

    project = models.ForeignKey(MusicTrackProject, models.CASCADE, 'instruments')
    name = models.CharField(max_length=25)
    notesColor = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='#ff0000',
    )

    @classmethod
    def define(cls, definition_name, default_settings):
        '''
        Объявляет новый тип инструмента (его стандартные настройки)

        :param definition_name: тип инструмента (из библиотеки Tone.js)
        :param default_settings: словарь со стандартными настройками, где значения настроек - это объекты класса `SettingValue`
        '''

        if 'volume' not in default_settings:
            default_settings = {
                'volume': FloatSettingValue(initial=-5.0, min_v=-50, max_v=50, step=0.5),
                **default_settings
            }
        return super().define(definition_name, default_settings)

    def to_dict(self):
        '''
        Возвращает словарь с данными и настройками
        музыкального инструмента
        '''

        return {
            **self.get_settings(),
            '_id': self.pk,
            '_type': self.type,
            '_notesColor': self.notesColor,
        }


class MusicInstrumentEffect(ModelWithSettings):
    '''
    **Модель эффекта музыкального инструмента**

    :param type: тип эффекта (из библиотеки Tone.js)
    :param instrument: инструмент
    '''

    instrument = models.ForeignKey(MusicInstrument, models.CASCADE, 'effects')


class MusicTrackPattern(models.Model):
    '''
    **Модель паттерна проекта**

    :param name: имя паттерна
    :param color: цвет паттерна в редакторе
    :param duration: продолжительность
    '''

    project = models.ForeignKey(MusicTrackProject, models.CASCADE, 'patterns')
    color = models.CharField(
        max_length=10,
        choices=COLOR_CHOICES,
        default='#0000ff',
    )
    name = models.CharField(max_length=25)
    duration = models.PositiveIntegerField(validators=[
        MinValueValidator(10),
        MaxValueValidator(256)
    ])

    def get_instruments(self):
        '''
        Возвращает инструменты, использующиеся в паттерне (генератор)
        '''

        pks = MusicNote.objects.filter(pattern=self)\
            .values_list('instrument', flat=True).distinct()
        for i_pk in pks:
            yield MusicInstrument.objects.get(pk=i_pk)

    def to_dict(self):
        '''
        Возвращает словарь с данными паттерна
        '''

        return {
            'id': self.id,
            'project_id': self.project_id,
            'name': self.name,
            'duration': self.duration,
            'color': self.color,
            'notes': list(MusicNote.objects.filter(pattern=self).values(
                'instrument', 'time', 'length', 'octave', 'notation',
            )),
        }


class TrackPatternInstance(models.Model):
    '''
    **Модель образца паттерна, который находиться на звуковой дорожке**

    :param pattern: паттерн
    :param time: момент времени, в который должен начать играть паттерн
    :param track: индекс звуковой дорожки на таймлайне
    '''

    pattern = models.ForeignKey(MusicTrackPattern, models.CASCADE, 'instances')
    time = models.PositiveIntegerField()
    track = models.PositiveIntegerField(
        validators=[MaxValueValidator(4)]
    )

    def to_dict(self):
        '''
        Возвращает словарь с данными образца паттерна
        '''

        return {
            'id': self.id,
            'pattern_id': self.pattern_id,
            'time': self.time,
            'track': self.track,
        }


class MusicNote(models.Model):
    '''
    **Модель музыкальной ноты в паттерне**

    :param pattern: паттерн
    :param time: момент времени, в который должна начать играть нота
    :param length: длительность ноты
    :param notation: буквенная нотация ноты
    :param octave: октава
    '''

    NOTATION_CHOICES = [
        (1, 'C'), (2, 'C#'),
        (3, 'D'), (4, 'D#'),
        (5, 'E'),
        (6, 'F'), (7, 'F#'),
        (8, 'G'), (9, 'G#'),
        (10, 'A'), (11, 'A#'),
        (12, 'B'),
    ]

    pattern = models.ForeignKey(MusicTrackPattern, models.CASCADE, 'notes')
    instrument = models.ForeignKey(MusicInstrument, models.CASCADE, 'notes')
    time = models.PositiveIntegerField()
    length = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    notation = models.PositiveIntegerField(choices=NOTATION_CHOICES)
    octave = models.PositiveIntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(7)]
    )
